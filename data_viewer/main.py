#!/usr/bin/env python

from data_viewer.controller import Controller
from data_viewer.views.tkview import TKView
from data_viewer.mocks import PlotterMock
from data_viewer.data_providers.csv_provider import CSVDataProvider

def main():
    data_provider = CSVDataProvider()
    plotter = PlotterMock()

    controller = Controller(data_provider, plotter)
    view = TKView(controller)
    controller.view = view

    controller.start()

if __name__== '__main__':
    main()

