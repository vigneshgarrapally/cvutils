import pandas as pd
from pathlib import Path
import shutil

# TODO Add tqdm progress bar

def csvtodirectory(csv_path, directory_path,move=False,xcol='image',ycol='label',dest_path='./output'):
    df=pd.read_csv(Path(csv_path))
    #df=df.sort_values(by=[ycol]).reset_index(drop=True)
    labels=df[ycol].unique()
    directory_path=Path(directory_path)
    dest_path=Path(dest_path)
    for label in labels:
        path=Path(dest_path,label)
        path.mkdir(exist_ok=True,parents=True)
    if not move:
        print(f"[INFO]Copy Started")
        #copy including metadata
        for label in labels:
            dest=Path(dest_path,label)
            if not dest.is_dir():
                raise Exception('destination directory Error')
            for image in list(df[df[ycol]==label][xcol]):
                src=Path(directory_path,image)
                shutil.copy2(str(src),str(dest))
        print(f"[INFO]Copied to {str(dest_path)}")
    else:
        print(f"[INFO]Move Started")
        #move dataset
        for label in labels:
            dest=Path(dest_path,label)
            if not dest.is_dir():
                raise Exception('destination directory Error')
            for image in list(df[df[ycol]==label][xcol]):
                src=Path(directory_path,image)
                shutil.move(str(src),str(dest))
        print(f"[INFO]Moved to {str(dest_path)}")


if __name__ == '__main__':
    import argparse
    myparser = argparse.ArgumentParser(description='Convert CSV Datasets to directory')
    myparser.add_argument('csv', type=str, help='csv file path')
    myparser.add_argument('directory', type=str, help='directory path')
    myparser.add_argument('--move', action='store_true', help='If specified move rather than copy')
    myparser.add_argument('--xcol', '-x',type=str, default='image', help='x column name')
    myparser.add_argument('--ycol', '-y',type=str, default='label', help='y column name')
    myparser.add_argument('--dest','-d', type=str, default='./output', help='destination path')
    args = myparser.parse_args()
    csvtodirectory(args.csv,args.directory,args.move,args.xcol,args.ycol,args.dest)
