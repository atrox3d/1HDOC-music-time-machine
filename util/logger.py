import os
import logging
import functools
import types
import inspect

# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future
# (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
from _ast import arguments


def get_cli_logger(what, level="DEBUG") -> logging.Logger:
    """
    ########################################################################################################################
        - GET LOCAL (NON-ROOT) LOGGER INSTANCE
        - SET LEVEL TO INFO (DEFAULT IS WARNING)
    ########################################################################################################################
    """
    # if classname is not None:
    # print(what.__name__)
    # if inspect.isclass(what):
    #     print("CLASS")
    #     _defaultlogger = logging.getLogger(what.__class__.__name__)  # get local logger
    # elif inspect.isfunction(what):
    #     print("FUNCTION")
    _defaultlogger = logging.getLogger(what.__qualname__)  # get local logger
    _defaultlogger.setLevel(level)  # set logger level >= INFO
    """
    ########################################################################################################################
        - GET SAME FORMATTER INSTANCE FOR ALL HANDLERS
    ########################################################################################################################
    """
    # if classname is not None:
    # if inspect.isclass(what):
    #     print("CLASS")
    #     formatstring = f'%(asctime)s | %(levelname)-8s | %(name)-10s | %(message)s'
    # elif inspect.isfunction(what):
    #     print("FUNCTION")
    formatstring = f'%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s'
    formatter = logging.Formatter(formatstring)  # get formatter
    """
    ########################################################################################################################
        - GET CLI HANDLER INSTANCE
        - SET FORMATTER FOR CLI HANDLER INSTANCE
        - ADD HANDLER TO LOCAL LOGGER
    ########################################################################################################################
    """
    cli_handler = logging.StreamHandler()  # get CLI handler (default=stderr)
    cli_handler.setFormatter(formatter)  # set formatter for CLI handler
    _defaultlogger.addHandler(cli_handler)  # add CLI handler to logger

    return _defaultlogger


def logger_arguments(ismethod, level="INFO"):
    # wraps decorator to pass arguments to the logger
    #
    # https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
    #
    _log = get_cli_logger(logger_arguments, "DEBUG")
    debug = True
    tabs = 1
    if debug: print(f"logger_arguments(ismethod={ismethod}, level={level})")

    def logger_decorator(func):
        #
        #   the decorator
        #
        nonlocal tabs
        tabs += 1
        if debug: print("\t" * tabs + f"logger_decorator(func={func.__qualname__})")
        _logger = get_cli_logger(func, level)

        @functools.wraps(func)
        def logger_wrapper(*args, **kwargs):
            # print(logger_wrapper.__name__)
            nonlocal tabs
            tabs += 1
            #
            #   the logger_wrapper
            #
            karguments = [f"{k}={v}" for k, v in kwargs.items()]  # list of "k=v" strings
            if ismethod:
                arguments = list(args[1:])  # remove self
            else:
                arguments = list(args)

            arguments.extend(karguments)  # join lists
            all_arguments = ', '.join(arguments)
            message = f"({all_arguments})"  # format message
            if len(message) > 67:  # format message
                message = message[:67] + " ..."  # format message

            if debug: print("\t" * tabs + f"logger_wrapper: call {func.__qualname__}({all_arguments})")

            _logger.info(message)  # log arguments before function
            _return = func(*args, **kwargs)  # execute function
            _logger.info("end")  # log after function
            #
            # return value of func
            #
            if debug: print("\t" * tabs + "logger_wrapper: return")
            return _return

        #
        #   return wrapped func
        #
        if debug: print("\t" * tabs + f"logger_decorator: return logger_wrapper {logger_wrapper.__qualname__}")
        return logger_wrapper

    #
    #   return logger decorator
    #
    if debug: print("logger_arguments: return logger_decorator")
    return logger_decorator


if __name__ == '__main__':
    logger = get_cli_logger()
    logger.debug('testing testing')
    logger.info('testing testing')
    logger.warning('testing testing')
    logger.error('testing testing')
    logger.critical('testing testing')

    logger = get_cli_logger('classname')
    logger.debug('testing testing')
    logger.info('testing testing')
    logger.warning('testing testing')
    logger.error('testing testing')
    logger.critical('testing testing')

    print(logger.handlers)
    print(logger.handlers[0])
    print(logger.handlers[0].formatter)
    print(logger.handlers[0].formatter._fmt)
