from GPUcard_detection import IR
import cv2

if __name__ == "__main__":
	detector = IR()
	while 1:
		ret = detector(1)
		if not ret:
			continue
		hands, img = ret
		cv2.imshow("frame", img)
		if hands:
			print(hands)
		key = cv2.waitKey(1)
		if key & 0xFF == ord('q'):
			break
