import cv2
import numpy as np
import gomoku

class PlayBoardProcessor():

    def __init__(self, instance:gomoku.GomokuGame):
        self.BOARD_SIZE=instance.BOARD_SIZE
        self.game_instance=instance
        self.avg_distances = None
        self.vid=cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.previous_state_board=[]
        self.pieces=None
        self.color_p1=self.game_instance.P1COL
        self.color_p2=self.game_instance.P2COL

    def calculate_euclidean_distance(self,p1, p2):
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def calculate_average_horizontal_vertical_distance(self,corners):
        corners = corners.reshape((self.BOARD_SIZE - 1, self.BOARD_SIZE - 1, 2))
    
        horizontal_distances = []
        vertical_distances = []

        for i in range(self.BOARD_SIZE - 1):
            for j in range(self.BOARD_SIZE - 1):
                p1 = corners[i, j]

                # add horizontal distances
                if j + 1 < self.BOARD_SIZE - 1:
                    p2 = corners[i, j + 1]
                    horizontal_distances.append(self.calculate_euclidean_distance(p1, p2))

                # add vertical distances
                if i + 1 < self.BOARD_SIZE - 1:
                    p3 = corners[i + 1, j]
                    vertical_distances.append(self.calculate_euclidean_distance(p1, p3))

        # calculate average distances
        avg_horizontal_distance = np.mean(horizontal_distances)
        avg_vertical_distance = np.mean(vertical_distances)

        return avg_horizontal_distance, avg_vertical_distance

    def extrapolate_full_board_corners(self,corners):
        avg_horizontal, avg_vertical = self.avg_distances

        full_board_corners = np.zeros((self.BOARD_SIZE + 1, self.BOARD_SIZE + 1, 2), dtype=np.float32)
        full_board_corners[1:-1, 1:-1] = corners.reshape((self.BOARD_SIZE - 1, self.BOARD_SIZE - 1, 2))

        for i in range(1, self.BOARD_SIZE):
            full_board_corners[i, -1] = [full_board_corners[i, -2, 0] + avg_horizontal, full_board_corners[i, -2, 1]]

        for j in range(1, self.BOARD_SIZE):
            full_board_corners[-1, j] = [full_board_corners[-2, j, 0], full_board_corners[-2, j, 1] + avg_vertical]

        for i in range(1, self.BOARD_SIZE):
            full_board_corners[i, 0] = [full_board_corners[i, 1, 0] - avg_horizontal, full_board_corners[i, 1, 1]]

        for j in range(1, self.BOARD_SIZE):
            full_board_corners[0, j] = [full_board_corners[1, j, 0], full_board_corners[1, j, 1] - avg_vertical]

        full_board_corners[0, 0] = [full_board_corners[1, 1, 0] - avg_horizontal, full_board_corners[1, 1, 1] - avg_vertical]
        full_board_corners[0, -1] = [full_board_corners[1, -2, 0] + avg_horizontal, full_board_corners[1, -2, 1] - avg_vertical]
        full_board_corners[-1, 0] = [full_board_corners[-2, 1, 0] - avg_horizontal, full_board_corners[-2, 1, 1] + avg_vertical]
        full_board_corners[-1, -1] = [full_board_corners[-2, -2, 0] + avg_horizontal, full_board_corners[-2, -2, 1] + avg_vertical]

        return full_board_corners

    def calculate_cell_centers(self,corners):
        centers = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                p1 = corners[i, j]
                p2 = corners[i, j + 1]
                p3 = corners[i + 1, j]
                p4 = corners[i + 1, j + 1]
                center_x = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
                center_y = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
                centers.append((center_x, center_y))
        return np.array(centers)

    def mark_pieces(self,cell_centers, img):    
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_blue = np.array([100, 150, 50])
            upper_blue = np.array([140, 255, 255])
    
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])

            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = mask_red1 + mask_red2
    
            blue_ellipses = self.detect_and_draw_ellipses(img, mask_blue, color=(255, 0, 0), shape="blue ellipses")
            red_ellipses = self.detect_and_draw_ellipses(img, mask_red, color=(0, 0, 255), shape="red ellipses")

            list_blue_shapes=self.match_shapes_to_centers(blue_ellipses, cell_centers, img,"blue")
            list_red_shapes=self.match_shapes_to_centers(red_ellipses, cell_centers, img,"red")

            print("detected",len(list_blue_shapes),"blue pieces")
            print("detected",len(list_red_shapes),"red pieces")

            list_shapes = list(set(list_blue_shapes + list_red_shapes))

            return list_shapes

    def detect_and_draw_ellipses(self,img, mask, color, shape="ellipses", min_area=50):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        min_area = (self.avg_horizontal * self.avg_vertical)/60
        max_area = (self.avg_horizontal * self.avg_vertical)+10
        detected_ellipses = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if max_area>=area >= min_area and len(cnt) >= 5:
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(img, ellipse, color, 2)
                center = (int(ellipse[0][0]), int(ellipse[0][1]))
                detected_ellipses.append(center)
    
        return detected_ellipses 

    def get_coordinates(self,index):
        x = index[0]//self.BOARD_SIZE
        y = index[0]%self.BOARD_SIZE
        return (x,y)

    def match_shapes_to_centers(self,shapes, cell_centers, img,color):

        list_shapes = []
        for shape in shapes:
            closest_center = None
            min_distance = float("inf")
        
            for center in cell_centers:
                distance = np.linalg.norm(np.array(shape) - np.array(center))
                if distance < min_distance:
                    min_distance = distance
                    closest_center = center
        
            max_distance=((self.avg_horizontal+self.avg_vertical)/2)*0.75

            if min_distance>max_distance:
                continue

            if closest_center.any():
                result=np.where(cell_centers == closest_center)
                index = (result[0][0], result[1][0])
                coordinates= self.get_coordinates(index)

                list_shapes.append((color,coordinates))


                shape_point = tuple(map(int, shape))  # Converteer shape naar een tuple van integers
                closest_center_point = tuple(map(int, closest_center))  # Converteer closest_center naar een tuple van integers
            

                # Teken een lijn van het object naar het dichtstbijzijnde celcentrum
                cv2.line(img, shape_point, closest_center_point, (0, 255, 0), 2)
                cv2.circle(img, shape_point, 5, (0, 255, 255), -1)  # Teken een geel punt op het gedetecteerde object
                cv2.circle(img, closest_center_point, 5, (255, 255, 0), -1)  # Teken een blauw punt op het celcentrum

        return list_shapes

    def get_move(self):
        number_of_inner_corners = (self.BOARD_SIZE - 1, self.BOARD_SIZE - 1)

        ret_img,img=self.vid.read()

        if not ret_img:
            print("Error: Could not read frame.")
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.medianBlur(gray, 13)
       
        ret, inner_corners = cv2.findChessboardCornersSB(gray, number_of_inner_corners,
                                                flags= cv2.CALIB_CB_EXHAUSTIVE +cv2.CALIB_CB_ACCURACY )
    
        if not ret:
            print("no chessboard detected at first")
            ret, inner_corners= cv2.findChessboardCorners(gray, number_of_inner_corners, flags= cv2.CALIB_CB_PLAIN +cv2.CALIB_CB_FAST_CHECK )

        if ret:
            print("Chessboard detected")
        
            inner_corners = cv2.cornerSubPix(gray, inner_corners, (11, 11), (-1, -1), 
                                        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        
            self.avg_distances = self.calculate_average_horizontal_vertical_distance(inner_corners)
            self.avg_horizontal, self.avg_vertical = self.avg_distances
        
            all_corners = self.extrapolate_full_board_corners(inner_corners)
        
            img_with_corners = img.copy()
            img_with_corners = cv2.drawChessboardCorners(img_with_corners, (self.BOARD_SIZE + 1, self.BOARD_SIZE + 1), all_corners.reshape(-1, 1, 2), ret)

            cell_centers = self.calculate_cell_centers(all_corners)

            self.pieces= self.mark_pieces(cell_centers,img.copy())

            color_current_player=self.game_instance.P1COL if gomoku.current_player==1 else self.game_instance.P2COL
            human_move=[]
            for piece in self.pieces:
                if piece not in self.previous_state_board and piece[0]==color_current_player:
                    print(piece,"detected")
                    human_move.append(piece[1])
            self.previous_state_board=self.pieces

            if len(human_move)==0:
                print("No move detected") #todo:show in GUI
            elif len(human_move)==1:
                print(human_move[0]) #todo: show last detected move in GUI
                return human_move
            else:
                print("Multiple moves detected") #todo: show in GUI

            return None

        else:
            print("No chessboard detected")
            return None
            #todo: add backup if possible