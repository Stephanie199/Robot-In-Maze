#ifndef ARENA_H
#define ARENA_H

#define ARENA_X_SIZE 20
#define ARENA_Y_SIZE 15
#define ARENA_UNIT_DISTANCE 10

#include <cstdlib>

enum GRIDTYPE{UNOCCUPIED = 0, OBSTACLE = 1, START = 2, GOAL = 3, UNEXPLORED = 4};

class Grid
{
public:
	GRIDTYPE type;
	bool isOnPath;
	bool opened;
	bool closed;
	int distanceTravelled;
	int distanceEstimated;
	int x, y, heuristic; // two way link coordination and heuristics
	Grid *parent;

	inline int getX() { return x; }
	inline int getY() { return y; }

	inline int Grid::getDistanceTravelled(Grid *p) { return p->distanceTravelled + ((x == p->x || y == p->y) ? 10 : 14); }
	inline int Grid::getDistanceEstimated(Grid *p) { return (abs(p->x - x) + abs(p->y - y)) * 10; }
	inline bool Grid::hasParent() { return parent != NULL; }
	void Grid::computeScores(Grid *end);
};

class Arena
{
public:
	Arena();
	~Arena();

	inline Grid* getGrid(int posX, int posY) { return &_grid[posX][posY]; }

	inline GRIDTYPE getGridType(int posX, int posY) { return _grid[posX][posY].type; }
	inline void setGridType(int posX, int posY, GRIDTYPE gridType) { _grid[posX][posY].type = gridType; }

	void init();
	bool isExploredFully();
	GRIDTYPE getRealGridType(int posX, int posY);

private:
	Grid _grid[ARENA_X_SIZE][ARENA_Y_SIZE];
};
#endif