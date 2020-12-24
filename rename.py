# Function to rename multiple files
import os
def main():
   i = 1704
   path="C:/Users/bkauy/OneDrive/Desktop/241_Final_Project/videos_and_frames/cleaned_individual_disengaged/"
   for filename in os.listdir(path):
      my_dest ="example" + str(i) + ".jpg"
      my_source = path + filename
      my_dest = path + my_dest
      # rename() function will
      # rename all the files
      os.rename(my_source, my_dest)
      i += 1
# Driver Code
if __name__ == '__main__':
   # Calling main() function
   main()


# path = working_dir + '/' + the_relative_path_you_gave_me
#
# working_dir = "c:/users/bkauyeung/engagement_app"
#
# path = 'c:/users/bkauyeung/engagement_app/Users\bkauy\engagement_app\app\static\img\photos'
