import cv2
import numpy as np
import pytesseract

# Configure tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- 1. Capture frame from camera ---
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

ret, frame = cap.read()
if not ret:
    print("Failed to grab frame")
    exit()

frame = cv2.resize(frame, (640, 480))

# --- 2. Convert to HSV for color detection ---
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define color ranges for pink and blue (adjust as needed)
pink_lower = np.array([140, 50, 50])
pink_upper = np.array([170, 255, 255])

blue_lower = np.array([90, 50, 50])
blue_upper = np.array([130, 255, 255])

mask_pink = cv2.inRange(hsv, pink_lower, pink_upper)
mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
mask = cv2.bitwise_or(mask_pink, mask_blue)

# --- 3. Find contours of tiles ---
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

tiles = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 1000:
        continue

    x, y, w, h = cv2.boundingRect(cnt)
    tile_img = frame[y:y+h, x:x+w]

    # OCR to read number
    gray = cv2.cvtColor(tile_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    text = pytesseract.image_to_string(thresh, config='--psm 10 -c tessedit_char_whitelist=0123456789')
    text = text.strip()

    if text.isdigit():
        tiles.append((x, y, int(text)))

# --- 4. Define grid size ---
# Example: 3 rows, 3 columns (change to match your grid)
rows = 4
cols = 4

# --- 5. Sort tiles into row-major order ---
# First sort by y (row), then x (column)
tiles_sorted = sorted(tiles, key=lambda t: (t[1], t[0]))

# Group tiles into rows based on y
row_threshold = 50  # pixels tolerance to group by row
grid = [[0]*cols for _ in range(rows)]  # initialize grid with 0s

row_index = 0
current_row_y = None
col_index = 0

for x, y, num in tiles_sorted:
    if current_row_y is None:
        current_row_y = y

    # Start a new row if y is far from current_row_y
    if abs(y - current_row_y) > row_threshold:
        row_index += 1
        col_index = 0
        current_row_y = y

    if row_index < rows and col_index < cols:
        grid[row_index][col_index] = num
        col_index += 1

# --- 6. Flatten row-major list ---
numbers_row_major = [num for row in grid for num in row]

print("Row-major tile numbers (0 = empty):", numbers_row_major)

# --- Optional: show frame with numbers ---
for x, y, num in tiles:
    try:
        # Draw rectangle around tile
        cv2.rectangle(frame, (x, y), (x+50, y+50), (0, 255, 0), 2)
        # Put the number above the tile
        cv2.putText(frame, str(num), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    except Exception as e:
        # Print error and continue
        print(f"Could not draw tile at ({x},{y}) with number {num}: {e}")

cv2.imshow("Tiles", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
