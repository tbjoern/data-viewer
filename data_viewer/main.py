#!/usr/bin/env python

from data_viewer.controller import Controller
from data_viewer.views.tkview import TKView
from data_viewer.plotter import MatplotlibPlotter
from data_viewer.data_providers.csv_provider import CSVDataProvider
from argparse import ArgumentParser

def main():

    parser = ArgumentParser()
    parser.add_argument('-d','--dir', help='opens the specified directory on program startup', nargs='*')
    args = parser.parse_args()

    data_provider = CSVDataProvider()
    plotter = MatplotlibPlotter()

    controller = Controller(data_provider, plotter)
    view = TKView(controller)
    controller.view = view

    if args.dir:
        print(args.dir)
        for d in args.dir:
            controller.open_path(d)

    controller.start()

if __name__== '__main__':
    main()

