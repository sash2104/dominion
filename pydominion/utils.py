def log(logger, brief, message):
    """ Logging function
    Parameters
    ----------
    logger: file_like
        logger must have a `write` method such as sys.stdout or file
    brief: str
        Brief message for log
    message: str
        A message to log
    """
    logger.write("[{}] {}\n".format(brief, message))
