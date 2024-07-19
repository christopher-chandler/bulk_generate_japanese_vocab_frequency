# Standard
import datetime


# Pip
# None

# Custom


"""
Hier sind Konstanten, die von anderen Funktionen verwendet werden. 
"""
current_datetime = datetime.datetime.now()
TIMESTAMP = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
SIMPLE_TIMESTAMP = current_datetime.strftime("%Y_%m_%d")


if __name__ == "__main__":
    pass
