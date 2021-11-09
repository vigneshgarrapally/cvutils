from utils import list_images
from pathlib import Path
import shutil
import pandas as pd
# TODO Add tqdm progress bar

def directorytocsv(directory,save_dir='./output',xcol='image',ycol='label',move=False,only_csv=False):
    directory = Path(directory)
    save_dir = Path(save_dir)
    if not save_dir.exists():
        save_dir.mkdir(exist_ok=True,parents=True)
    if not directory.is_dir():
        raise Exception('{} is not a directory'.format(str(directory)))
    if not save_dir.is_dir():
        raise Exception('{} is not a directory'.format(str(save_dir)))
    labels=list(map(lambda x: x.name,directory.iterdir()))
    image_list = list_images(directory)
    df_list=list()
    Path(save_dir,"images").mkdir(exist_ok=True,parents=True)
    for image in image_list:
        dest=Path(save_dir,'images',image.name)
        if (not only_csv) and move:
            shutil.move(str(image),str(dest))
        elif not (only_csv and move):
            shutil.copy2(str(image),str(dest))
        if image.parent.name in labels:
            # TODO append to csv
            df_list.append([str(image.name),str(image.parent.name)])
        else:
            raise Exception(f"{image} is corrupted")
    df = pd.DataFrame(df_list,columns=[xcol,ycol])
    df.to_csv(Path(save_dir,'labels.csv'),index=False)
    print("[INFO] Completed")
        



if __name__ == "__main__":
    import argparse
    myparser = argparse.ArgumentParser(description='Convert a ImageDirectory to a CSV')
    myparser.add_argument('directory',type=str,help='path to Image Directory')
    myparser.add_argument('--dest','-d',type=str,help='Directory to save the CSV Dataset',default='./output')
    myparser.add_argument('--xcol','-x',type=str,help='Column name for the image path',default='image')
    myparser.add_argument('--ycol','-y',type=str,help='Column name for the label',default='label')
    myparser.add_argument('--move','-m',action='store_true',help='Move the images to the output directory',default=False)
    myparser.add_argument('--only_csv','-o',action='store_true',help='Only create the CSV file',default=False)
    args = myparser.parse_args()
    directorytocsv(args.directory,args.dest,args.xcol,args.ycol,args.move,args.only_csv)