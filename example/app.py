#!/usr/bin/env python3
from simpletailer import SimpleTailer

if __name__ == "__main__":
    try:
        for line in SimpleTailer("mylog.file"):
            print(line)
    except KeyboardInterrupt:
        pass
