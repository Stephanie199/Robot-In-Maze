#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#define ROBOT_SIZE 2

#include <gtkmm.h>
#include "Arena.h"
#include "displayItem.h"
#include "robot.h"
#include "MapIO.h"
#include "pathfinder.h"

class MainWindow : public Gtk::Window
{
public:
	MainWindow();
	virtual ~MainWindow();
protected:
	// identity members
	Arena* arena;
	Robot* robot;
	Arena* fullArena;
	MapIO* io;
	PathFinder* pathFinder;
	Connector* conn;
	// display members
	Gtk::Table arenaDisplay;
	DisplayItem *gridDisplay[ARENA_X_SIZE][ARENA_Y_SIZE];
	Gtk::VBox vbox;
	Gtk::HBox hbox;
	Gtk::Button startExploration;
	Gtk::Entry percentageEntry, timeLimitEntry;

	// signal handler
	void MainWindow::startExplorationButtonClicked();

private:
	void hideRobot(int x, int y);
	void displayRobot(int x, int y);
	void refreshAllDisplay();

	// real time update functions
	bool MainWindow::exploreProcessHandler();
	bool MainWindow::shortestPathHandler();
	std::vector<std::pair<std::string, int>*>* movementList;
	std::vector<Grid*> result;
	std::vector<std::pair<std::string, int>*>::iterator i;
	bool waitDone;
	int range;
};

#endif