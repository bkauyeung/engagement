# Function to rename multiple files
# def main():
#    i = 0
#    path="C:/Users/bkauy/engagement_app/app/static/img/photos/"
#    for filename in os.listdir(path):
#       my_dest ="example" + str(i) + ".jpg"
#       my_source = path + filename
#       my_dest = path + my_dest
#       # rename() function will
#       # rename all the files
#       os.rename(my_source, my_dest)
#       i += 1
# # Driver Code
# if __name__ == '__main__':
#    # Calling main() function
#    main()


import os
hists = os.listdir("photos/")
hists = ['img/photos' + file for file in hists]
print(hists)

# path = working_dir + '/' + the_relative_path_you_gave_me
#
# working_dir = "c:/users/bkauyeung/engagement_app"
#
# path = 'c:/users/bkauyeung/engagement_app/Users\bkauy\engagement_app\app\static\img\photos'
