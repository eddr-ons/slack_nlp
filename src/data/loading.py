import os
import glob
import logging

import pandas as pd


def json_to_df(raw_data_dir = "../data/raw/",
               slack_dir = "slack channels",
               save_dir = "../data/interim/",
               csv_name = "slack_data.csv",
               save_to_csv = False,
               verbose = False,
               log_fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
              ):
    """
    takes the json files from the slack dump and puts them in a single
    DataFrame and returns with the option of saving to csv. Also adds a new
    column variable 'channel' with the name of the folder the json contianing
    the observation was found in

    Args:
        raw_data_dir: where slack_dir is relative to the current directory
        slack_dir: the folder containing sub_folders for each channel with the jsons
        save_dir: folder to save csv to relative to current directory
        csv_name: name of the csv
        save_to_csv: set to True for saving to csv
        verbose: output logging messages
        log_fmt: logging format


    Returns: pandas DataFrame containing data from json files.
        rows give observations, columns give variables found in jsons

    """

    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    else:
        logging.basicConfig(level=logging.INFO, format=log_fmt)

    logger.info('Creating DataFrame from jsons')

    channel_dir = "{}{}".format(raw_data_dir, slack_dir)

    # get the channel folders containing jsons
    folder_lst = [folder
                  for folder in os.listdir(channel_dir)
                  if os.path.isdir("{}/{}".format(channel_dir, folder))
                  ]

    channel_lst = []
    logger.info('loading jsons from...')

    for folder in folder_lst:

        logger.info('\t{}'.format(folder))
        path = "{}/{}".format(channel_dir, folder)
        # get all json in folder, load each to dataframe in list comp and concat to single df
        channel_df = pd.concat([pd.read_json(file)
                                for file in glob.glob(path + "/*.json")
                                ])
        # add channel as a variable
        channel_df["channel"] = folder
        channel_lst.append(channel_df)

    logger.info('concatenating data to single DataFrame')
    # since we add channels as a variable we need to do the concat in two steps
    df = pd.concat(channel_lst)

    # save if we want
    if save_to_csv:
        logger.info('saving to {}{}'.format(save_dir, csv_name))
        df.to_csv("{}{}".format(save_dir, csv_name))

    return df

