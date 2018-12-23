import logging
import re

import pandas as pd

from gensim.parsing.preprocessing import strip_numeric, strip_punctuation, strip_tags, strip_multiple_whitespaces, strip_short, remove_stopwords



def format_ts(df,
              time_cols = ["latest_reply","thread_ts", "ts"],
              unit_time = "s",
              save_dir="../data/interim/",
              csv_name="slack_data_ts.csv",
              save_to_csv=False,
              verbose = False,
              log_fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

              ):
    """

    Args:
        df:
        time_cols:
        unit_time:
        save_dir:
        csv_name:
        save_to_csv:

    Returns:

    """
    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    else:
        logging.basicConfig(level=logging.INFO, format=log_fmt)

    logger.info('converting columns to timedate format')

    for col in time_cols:
        logger.info('...{}'.format(col))
        df[col] = pd.to_datetime(df[col], unit= unit_time)

        # save if we want
    if save_to_csv:
        logger.info('saving to {}{}'.format(save_dir, csv_name))
        df.to_csv("{}{}".format(save_dir, csv_name))

    return df


def tokenise_text_col(df, text_col="text", suffix="_tokens", return_col_name = False):

    """
    wrapper function for a list comprehenshion that tokenises a text column
    in df, returning df with a new column containing tokenised text
    Args:
        df: dataframe with text data
        text_col: column with text data
        suffix: to add to text_col to give the column name containing tokenised text
        return_col_name: flag to return col name or not
    Returns:
        pandas dataframe with new column containing tokenised text and the column name if
        return_col_name flag is true
    """
    col_name = text_col + suffix
    df[col_name] = [text.split(" ")
                             for text in df[text_col].astype(str).tolist()
                             ]
    if return_col_name:
        return df, col_name
    else:
        return df


def to_lower(df, token_col = "text_tokens"):

    """
    Turns tokenised text to lowercase
    converts tokenised text lists in toke_col to lowercase
    Args:
        df: dataframe with tokenised lists
        token_col: column in df containing tokenised lists

    Returns: df with text in token_col converted to lowercase

    """

    proc_words = []
    for words in df[token_col]:
        # convert to lower case
        proc_words.append([word.lower()
                           for word in words
                           ])
    df[token_col] = proc_words

    return df

def remove_links(df, token_col="text_tokens"):

    """
    Removes links (all text between < and >) in tokenised column
    Args:
        df (DataFrame): dataframe containing tokenised text
        token_col (string): column in df containitng tokenised text

    Returns: df with links removed from tokenised text

    """
    proc_words = []
    for words in df[token_col]:
        proc_words.append([re.sub('<[^>]+>', "", word)
                           for word in words
                           ])

    df[token_col] = proc_words
    return df


def remove_blanks(df, token_col="text_tokens"):
    """
    removes blank elements in tokenised text column in df if there are non blank elements  in that list
    Args:
        df (DataFrame): dataframe containing tokenised text
        token_col (string): column in df containitng tokenised text


    Returns: df with blank words inside tokenised lists removed

    """
    proc_words = []
    for words in df[token_col]:
        # is list not empty?
        if words:
            # remove empty strings
            proc_words.append([word
                               for word in words
                               if word
                               ])
        else:
            # add empty list if list is empty, to keep list size the same
            proc_words.append([])

    df[token_col] = proc_words
    return df


def text_proc_pipeline(df,
                       text_col="text",
                       unproc_suffix="_unproc",
                       stopword_suffix="_no_stopwords",
                       min_word_size=2,
                       verbose=False,
                       log_fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                       ):

    """

    Args:
        df (dataframe): contains text to process
        text_col (str): column in df containing text to process
        unproc_suffix (str): column suffix for text_col where unprocessed text is stored
        stopword_suffix (str): column suffix for text_col where stopword removed text is stored
        min_word_size (int): remove words of length less than this
        verbose (bool): output logging messages
        log_fmt (str): format for log messages

    Returns: Dataframe with processed text, including stopwords in text_col, processed text without stopwords in
        text_col+stopword_suffix and the unprocessed text in text_col+unproc_suffix

    """

    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    else:
        logging.basicConfig(level=logging.INFO, format=log_fmt)

    logger.info('starting processing pipeline')
    logger.info('storing unprocessed text in {}{}'.format(text_col, unproc_suffix))
    df[text_col+unproc_suffix] = df[text_col]

    # remove html tags
    logger.info('removing html')
    df[text_col] = [strip_tags(text)
                    for text in df[text_col].astype(str).tolist()
                    ]

    # remove multiple spaces, tabs etc.
    logger.info('removing multiple spaces')
    df[text_col] = [strip_multiple_whitespaces(text)
                    for text in df[text_col].astype(str).tolist()
                    ]

    # remove punctuation
    logger.info('removing punctuation')
    df[text_col] = [strip_punctuation(text)
                    for text in df[text_col].astype(str).tolist()
                    ]

    # remove numbers
    logger.info('removing numeric')
    df[text_col] = [strip_numeric(text)
                    for text in df[text_col].astype(str).tolist()
                    ]

    # get rid of single characters
    logger.info('removing characters less than {}'.format(min_word_size))
    df[text_col] = [strip_short(text, minsize=min_word_size)
                    for text in df[text_col].astype(str).tolist()
                    ]
    # to lowercase
    logger.info('converting text to lower case')
    df[text_col] = df[text_col].str.lower()

    # remove stopwords. we store in another column as they may or may not improve the model
    logger.info('removing stopwords; stored in {}{}'.format(text_col, stopword_suffix))
    df[text_col+stopword_suffix] = [remove_stopwords(text)
                                    for text in df[text_col].astype(str).tolist()
                                    ]
    logger.info('complete')

    return df








