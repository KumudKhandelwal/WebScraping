# do the necessary imports
import os       # for performing system operations

# function to compare the two folders
def folder_diff(path_folder1, path_folder2):
    folder1_list = os.listdir(path_folder1)
    folder2_list = os.listdir(path_folder2)
    # create a blank list
    missing_files = []
    # For each file in folder1, check if it exists in folder2 as well.
    # If found, skip. Otherwise, append the missing file to the list
    for item in folder1_list:
        if os.path.exists(f'{path_folder2}/{item}'):
            continue
        else:
            missing_files.append(item)
    # return all the missing files
    return missing_files

# execute the below code if run directly and not via import in some other module
if __name__ == "__main__":
    
    # path to the folder which has more files
    # path_folder1 = 'scrapyenv/scraper/scraper/supporting_files/lin_scraped_HTMLs'
    path_folder1 = '/home/lincoln/Internship_Project/readability_batch/readability_python/html_files_in'
    # path to the folder which has less files
    # path_folder2 = 'scrapyenv/scraper/scraper/supporting_files/lin_readability_processed_HTMLs'
    path_folder2 = '/home/lincoln/Internship_Project/readability_batch/readability_python/html_files_out'
    # path to the file which will record the difference in files
    # diff_file = 'scrapyenv/scraper/scraper/supporting_files/diff_files'
    diff_file = '/home/lincoln/Internship_Project/readability_batch/readability_python/abc_out/in_out_diff_files'
    
    # delete this file if already exists. We will create it fresh later on with the updated data.
    if os.path.exists(diff_file):
        os.remove(diff_file)
        
    # check for file difference
    diff_data = folder_diff(path_folder1, path_folder2)
    # record the differences in the file we just created
    for item in diff_data:
        # initialize mode as 'append mode'
        mode = 'a'
        if not os.path.exists(diff_file):
            mode = 'w'
        # open the file and write the data into it
        with open(diff_file, mode) as f:
            f.write(item)
            f.write('\n')