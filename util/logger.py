import sys
import logging
import functools


# import os
# import types
# import inspect
# from _ast import arguments

##################################################################################################################
# logging.NOTSET | "NOTSET" | 0:
#       Detailed information, typically of interest only when diagnosing problems.
# logging.DEBUG | "DEBUG" | 10:
#       Detailed information, typically of interest only when diagnosing problems.
# logging.INFO | "INFO" | 20:
#       Confirmation that things are working as expected.
# logging.WARNING | "WARNING" | 30:
#       An indication that something unexpected happened, or indicative of some problem in the near future
#       (e.g. ‘disk space low’). The software is still working as expected.
# logging.ERROR | "ERROR" | 40:
#       Due to a more serious problem, the software has not been able to perform some function.
# logging.CRITICAL | "CRITICAL" | 50:
#       A serious error, indicating that the program itself may be unable to continue running.
##################################################################################################################


def get_cli_logger(
        name,
        level="DEBUG",
        set_handler=True,
        format_sring=f'%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s',
        output_stream=sys.stderr,
) -> logging.Logger:
    """
    ########################################################################################################################
        - GET LOCAL (NON-ROOT) LOGGER INSTANCE THAT OUTPUTS TO CLI
        - SET LEVEL TO DEBUG (DEFAULT IS WARNING)
    ########################################################################################################################
    """
    _logger = logging.getLogger(name)  # get local logger
    _logger.setLevel(level)  # set logger level >= logger_level
    """
    ########################################################################################################################
        - GET SAME FORMATTER INSTANCE FOR ALL HANDLERS
    ########################################################################################################################
    """
    formatstring = format_sring
    formatter = logging.Formatter(formatstring)  # get formatter
    """
    ########################################################################################################################
        - GET CLI HANDLER INSTANCE
        - SET FORMATTER FOR CLI HANDLER INSTANCE
        - ADD HANDLER TO LOCAL LOGGER
    ########################################################################################################################
    """
    if set_handler and not _logger.hasHandlers():
        cli_handler = logging.StreamHandler(stream=output_stream)  # get CLI handler (default=stderr)
        cli_handler.setFormatter(formatter)  # set formatter for CLI handler
        _logger.addHandler(cli_handler)  # add CLI handler to logger

    return _logger


def get_child_logger(parent, name):
    if isinstance(parent, str):
        return logging.getLogger(parent).getChild(name)
    elif isinstance(parent, logging.Logger):
        return parent.getChild(name)
    else:
        raise TypeError


def logger_decorator_with_arguments(
        ismethod,  # is ismethod == True ignore self when logging arguments
        func_logging_level="INFO"  # logging level for decorated function
):
    """
    wraps decorator to pass arguments to the logger
    https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
    """
    tabs = 1
    debuggers = []
    debuggers.append(get_child_logger(_module_logger, "arguments"))
    debugger = debuggers[-1]
    #
    #   this will be output only if the module debugger is set to DEBUG
    #
    debugger.debug(f"logger_arguments(ismethod={ismethod}, level={func_logging_level})")

    #
    #   create decorator
    #
    def logger_decorator(func):
        #
        #   the decorator
        #
        nonlocal tabs  # increase tab width for every inner function
        tabs += 1

        # debugger = get_cli_logger("util.logger.arguments.decorator", set_handler=False, level="NOTSET")
        debuggers.append(get_child_logger(debuggers[-1], "decorator"))
        debugger = debuggers[-1]
        #
        #   this will be output only if the module debugger is set to DEBUG
        #
        debugger.debug("\t" * tabs + f"logger_decorator(func={func.__qualname__})")

        @functools.wraps(func)
        def logger_wrapper(*args, **kwargs):
            #
            #   the logger_wrapper
            #
            nonlocal tabs
            tabs += 1

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

            # debuggers = get_cli_logger("util.logger.arguments.decorator.wrapper", set_handler=False, level="NOTSET")
            debuggers.append(get_child_logger(debuggers[-1], "wrapper"))
            debugger = debuggers[-1]
            debugger.debug("\t" * tabs + f"logger_wrapper: call {func.__qualname__}({all_arguments})")

            _logger = get_cli_logger(func.__qualname__, func_logging_level)
            # logger_wrapper.logger = _logger # attach logger to function (wrapped) as attribute
            # print(logger_wrapper.logger)
            _logger.info(message)  # log arguments before function
            _return = func(*args, **kwargs)  # execute function
            _logger.info("end")  # log after function
            #
            # return value of func
            #
            debugger.debug("\t" * tabs + "logger_wrapper: return")
            return _return

        #
        #   return wrapped func
        #
        debugger.debug("\t" * tabs + f"logger_decorator: return logger_wrapper {logger_wrapper.__qualname__}")
        return logger_wrapper

    #
    #   return logger decorator
    #
    debugger.debug("logger_arguments: return logger_decorator")
    return logger_decorator


def enable():
    logging.disable(logging.NOTSET)


def disable():
    logging.disable(logging.CRITICAL)


#
#   create parent logger for module
#
_module_logger = get_cli_logger(
    # "util.logger",
    __name__,
    # level="DEBUG",
    output_stream=sys.stdout
)
_module_logger.setLevel(logging.INFO)  # do not show children's debug log

if __name__ == '__main__':
    logger = get_cli_logger("test." + __name__)
    logger.debug('testing testing')
    logger.info('testing testing')
    logger.warning('testing testing')
    logger.error('testing testing')
    logger.critical('testing testing')

    logger = get_cli_logger('test.classname')
    logger.debug('testing testing')
    logger.info('testing testing')
    logger.warning('testing testing')
    logger.error('testing testing')
    logger.critical('testing testing')

    print(logger.handlers)
    print(logger.handlers[0])
    print(logger.handlers[0].formatter)
    print(logger.handlers[0].formatter._fmt)
