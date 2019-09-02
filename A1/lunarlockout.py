'''Lunar Lockout routines.

    A) Class LunarLockoutState

    A specializion of the StateSpace Class that is tailored to the game of LunarLockout.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in LunarLockout.

    Code also contains LunarLockout problems for the purpose of testing.
'''

from search import *
import random 

class LunarLockoutState(StateSpace):

    def __init__(self, action, gval, parent, size, robots, xanadus):
        '''
        Creates a new LunarLockoutState state.
        @param width: The room's X dimension (excluding walls).
        @param height: The room's Y dimension (excluding walls).
        @param robots: A tuple of all the robots' locations. Each robot is denoted by its index in the list. 
        @param xanadus: A tuple of all the xanadus' locations. Each xanadus is denoted by its index in the list. 
        '''

        if ((size%2)==0): 
          size = size+1
          print("Boards must be of odd dimension. Board has been enlardged by one block.")

        StateSpace.__init__(self, action, gval, parent)
        self.width = size
        self.height = size

        self.robots = robots 
        self.xanadus = xanadus 

    def getRobots(self):
      return self.robots

      
    def successors(self):
        '''
        Generates all the actions that can be performed from this state, and the states those actions will create.        
        '''

        successors = []
        transition_cost = 1
        center = int((self.width-1)/2)

        for robot in range(0, len(self.robots)):
          other_robots = list(self.robots);
          other_robots.remove(self.robots[robot])

          if(isinstance(self.xanadus[0],int)):
            other_robots = tuple(other_robots) + (self.xanadus,)
          else:
            # remove any xanadus that are already in the center
            xanadubots = [i for i in self.xanadus if i[0] != center or i[1] != center]            
            other_robots = tuple(other_robots) + tuple(xanadubots)

          for direction in (UP, RIGHT, DOWN, LEFT):

              new_location = direction.move(self.robots[robot], other_robots)
              if new_location == None:
                continue
              if new_location[0] < 0 or new_location[0] >= self.width:
                  continue
              if new_location[1] < 0 or new_location[1] >= self.height:
                  continue
              if new_location in other_robots:
                  continue

              new_robots = list(self.robots)
              new_robots[robot] = new_location
              new_robots = tuple(new_robots)

              new_state = LunarLockoutState(chr(ord('a') + robot) + " " + direction.name, self.gval + transition_cost, self, self.width, new_robots, self.xanadus)
              successors.append(new_state)

        if(isinstance(self.xanadus[0],int)):
          stop_index = 1
        else:
          stop_index = len(self.xanadus)

        for robot in range(0, stop_index):
          other_robots = list(self.xanadus);
          if(isinstance(other_robots[0],int)):
            other_robots = self.robots
            xanadu = self.xanadus
          else:
            xanadu = self.xanadus[robot]
            if xanadu[0] == center and xanadu[1] == center:
              continue
            other_robots.remove(self.xanadus[robot])
            other_robots = [x for x in other_robots if (x[0]!=center or x[1]!=center)]
            other_robots = tuple(other_robots) + self.robots            
            
          for direction in (UP, RIGHT, DOWN, LEFT):
              new_location = direction.move(xanadu, other_robots)

              if new_location == None:
                continue
              if new_location[0] < 0 or new_location[0] >= self.width:
                  continue
              if new_location[1] < 0 or new_location[1] >= self.height:
                  continue
              if new_location in other_robots:
                if new_location[0] != center and new_location[1] != center:
                  continue

              if (isinstance(self.xanadus[0], int)):
                new_xanadus = new_location
              else:
                new_xanadus = list(self.xanadus)
                new_xanadus[robot] = new_location
                new_xanadus = tuple(new_xanadus)

              new_state = LunarLockoutState(chr(ord('A') + robot) + " " + direction.name, self.gval + transition_cost, self, self.width, self.robots, new_xanadus)
              successors.append(new_state)

        return successors

    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent a state.'''
        return hash((self.robots, self.xanadus))       

    def state_string(self):
        '''Returns a string representation fo a state that can be printed to stdout.'''        
        center = (self.width-1)/2

        map = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]
        
        if(isinstance(self.xanadus[0],int)):
          if self.xanadus[0] == center and self.xanadus[1] == center:
            map[self.xanadus[1]][self.xanadus[0]] = chr(ord('*'))
          else:
            map[self.xanadus[1]][self.xanadus[0]] = chr(ord('A'))
        else:
          for i, robot in enumerate(self.xanadus):
            if robot[0] == center and robot[1] == center:
              map[robot[1]][robot[0]] = chr(ord('*'))
            else:
              map[robot[1]][robot[0]] = chr(ord('A') + i)          

        for i, robot in enumerate(self.robots):
            map[robot[1]][robot[0]] = chr(ord('a') + i)
        
        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]

        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'

        return s        

    def print_state(self):
        '''
        Prints the string representation of the state. ASCII art FTW!
        '''        
        print("ACTION was " + self.action)      
        print(self.state_string())


def lockout_goal_state(state):
  '''Returns True if we have reached a goal state'''
  '''INPUT: a LunarLockout state'''
  '''OUTPUT: True (if goal) or False (if not)'''  
  center = int((state.width-1)/2)

  if (isinstance(state.xanadus[0], int)):
    if (state.xanadus[1] != center or state.xanadus[0] != center):
        return False
  else:
    for robot in state.xanadus:
      test_center = list(robot)
      if (test_center[1] != center or test_center[0] != center):
        return False

  return True

#LunarLockout Directions: encodes directions of movement that are possible for each robot.
class Direction():
    '''
    A direction of movement.
    '''
    
    def __init__(self, name, delta):
        '''
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction.
        '''
        self.name = name
        self.delta = delta
    
    def __hash__(self):
        '''
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        '''
        return hash(self.name)
    
    def __str__(self):
        '''
        @return: The string representation of this object when *str* is called.
        '''
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    def move(self, location, other_robots):

        ''' only move robots when there is another robot in same row or same column '''
        delta = self.delta;
        change = (99,99)

        if (delta[0] == 0):
          relevant_robots = [other_robots[i] for i in range(len(other_robots)) if other_robots[i][0] == location[0]]
          if (len(relevant_robots) == 0): 
            return
          ylocs = [y[1] for y in relevant_robots]
          positions = [y-location[1] for y in ylocs]
          direction = delta[1]
          change = (0,99)
        else:          
          relevant_robots = [other_robots[i] for i in range(len(other_robots)) if other_robots[i][1] == location[1]]
          if (len(relevant_robots) == 0): 
            return          
          xlocs = [x[0] for x in relevant_robots]
          positions = [x-location[0] for x in xlocs]
          direction = delta[0]
          change = (99,0)

        if (direction == -1):  
          positions = [positions[i] for i in range(len(positions)) if positions[i] < 0]
          if (len(positions) == 0):
            return
          value = max(positions)+1

        else:  
          positions = [positions[i] for i in range(len(positions)) if positions[i] > 0]
          if (len(positions) == 0):
            return
          value = min(positions)-1    

        change = [value if x==99 else x for x in change]  

        if (change[0] + change[1] == 0):
          return

        return (location[0] + change[0], location[1] + change[1])


#Global Directions
UP = Direction("up", (0, -1))
RIGHT = Direction("right", (1, 0))
DOWN = Direction("down", (0, 1))
LEFT = Direction("left", (-1, 0))
