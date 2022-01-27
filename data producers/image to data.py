import os
import cv2
import csv


def rewerite_data(file_loc, loc_time):
    with open(os.path.join(file_loc, 'data.txt'), 'r') as f:
        lines = f.readlines()
        f.close()

    if len(lines) < 12:
        with open(os.path.join(file_loc, 'data.txt'), 'w') as f:
            for line in lines[:3]:
                f.write(line)
            line = lines[3].split()
            f.write(f"Half_stars: {line[2]}\n")
            f.write(lines[4])
            f.write(f"Session:{loc_time}\n")
            line = lines[5].split()
            f.write(f"Local_time: {line[1]}\n")
            for line in lines[6:]:
                f.write(line)
            f.close()


def click_event(event, x, y, a, b):
    """
    An event which opens an image to click upon and record point on image.
    Parameters
    ----------
    x y - the x,y coordinates of the mouse pointer
    a,b - I have no idea why these parameters are necessary as they aren't used, but trust me, do not delete them,
          I went down that rabbit hole

    Returns
    -------
    mouse_coor - appends x,y into a global variable
    click_count - a click counter, once it reaches 4 clicks terminating the event
    """
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        print(x, ' ', y)
        coor = [x, y]
        cv2.line(img, (coor[0], coor[1]), (coor[0] + crop_sze[0], coor[1]), (0, 0, 255), 2)
        cv2.line(img, (coor[0], coor[1]), (coor[0], coor[1] + crop_sze[1]), (0, 0, 255), 2)
        cv2.line(img, (coor[0], coor[1] + crop_sze[1]), (coor[0] + crop_sze[0], coor[1] + crop_sze[1]), (0, 0, 255), 2)
        cv2.line(img, (coor[0] + crop_sze[0], coor[1]), (coor[0] + crop_sze[0], coor[1] + crop_sze[1]), (0, 0, 255), 2)
        cv2.imshow('image', img)
        cv2.waitKey()


def del_imgs_from_set(folder: str, csv_name: str):
    """
    In case you want to delete some photos from the dataset call this function afterwards. It goes over all csv lines
    and checks if each image is present, if an image isn't, the function renames the last image in the folder to fill
    the missing place and changes the csv file accordingly.
    ----------
    folder - the folder path where the images are
    csv_name - name of the csv file

    Returns
    -------
    None
    """
    labels = []
    csv_path = os.path.join(folder, csv_name)
    file = open(csv_path, "r")
    csv_reader = csv.reader(file)
    for row in csv_reader:
        labels.append(row)

    i, j = 1, len(labels) - 1
    while i < len(labels):
        if not os.path.isfile(os.path.join(folder, labels[i][0][:-1])):
            j = len(labels) - 1
            while not os.path.isfile(os.path.join(folder, labels[j][0][:-1])):
                labels.pop()
                j -= 1
            if j <= i:
                labels = labels[:i]
                break
            os.rename(os.path.join(folder, labels[j][0][:-1]), os.path.join(folder, labels[i][0][:-1]))
            labels[i][1:] = labels.pop(j)[1:]
        i += 1

    with open(csv_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for line in labels:
            csv_writer.writerow(line)


# ------------------------------------- main ------------------------------------------------ #
if __name__ == '__main__':
    inp_file_path = os.path.join(os.getcwd(), 'images')
    out_file_path = os.path.join(os.getcwd(), 'images')
    del_imgs_from_set(out_file_path, 'labels.csv')

    crop_sze = [512, 256]  # the images size desired output

    flag_take_coor = False
    if flag_take_coor:
        img = cv2.imread(os.path.join(inp_file_path, 'image'))
        while True:
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', click_event)
            # wait for a key to be pressed to exit
            cv2.waitKey()
            cv2.destroyAllWindows()
            value = input('Are you happy with these results? (y\\n)')
            if value == 'y':
                break


    #
    # scale_fac = 0.5                              # image resize scale
    # flag_take_coor = False
    # flag_crop = False
    # flag_save = False
    #
    # # open the existing csv file in the processed data folder and find the number of images already stored
    # if os.path.isfile(os.path.join(out_file_path, 'labels.csv')):
    #     with open(os.path.join(out_file_path, 'labels.csv'), mode='r', newline='') as csvfile:
    #         file_reader = csv.reader(csvfile)
    #         counter = len(list(file_reader))
    # else:
    #     with open(os.path.join(out_file_path, 'labels.csv'), mode='w', newline='') as csvfile:
    #         csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #         csv_writer.writerow(['Picture no.', 'Location', 'URL', 'Stars', 'Half_stars', 'Swell', 'Session',
    #                              'Local_time', 'Sunrise', 'Sunset', 'Weekday', 'Weather', 'Crop_Point'])
    #         counter = 1
    #
    # subfolders = [f.path for f in os.scandir(inp_file_path) if f.is_dir()]
    # for folder in subfolders:
    #     with open(os.path.join(folder, 'data.txt'), 'r') as f:
    #         lines = f.readlines()
    #         f.close()
    #
    #     strt_pnt = [int(lines[11].split(' ')[1]), int(lines[11].split(' ')[2])]
    #
    #     if flag_save:
    #         for i in range(1, len(lines)):
    #             lines[i] = ' '.join(lines[i].split()[1:]) + '\n'
    #
    #     for file in os.listdir(folder):
    #         filename = os.fsdecode(file)
    #         if filename.endswith('.png'):
    #             img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_UNCHANGED)

    #             # crop area of interest
    #             if flag_crop:
    #                 img = img[strt_pnt[1]:strt_pnt[1]+crop_sze[1], strt_pnt[0]:strt_pnt[0]+crop_sze[0], :]
    #
    #             # resize image
    #             width = int(img.shape[1] * scale_fac)
    #             height = int(img.shape[0] * scale_fac)
    #             dim = (width, height)
    #             img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    #
    #             if flag_save:
    #                 cv2.imwrite(os.path.join(out_file_path, 'image' + str(counter) + '.png'), img)
    #                 with open(os.path.join(out_file_path, 'labels.csv'), mode='a', newline='') as csvfile:
    #                     csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #                     csv_writer.writerow(['image' + str(counter) + '.png\n'] + lines)
    #             counter += 1
    #         else:
    #             continue
