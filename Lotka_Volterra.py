"""
Python model "Lotka_Volterra.py"
Translated using PySD version 1.4.0
"""
from os import path
from scipy import interpolate

from pysd.py_backend.functions import Integ
from pysd import cache

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Area": "area",
    "Initial Lynx Population": "initial_lynx_population",
    "Initial Hare Population": "initial_hare_population",
    "Initial Wolf Population": "initial_wolf_population",
    "Lynx Births": "lynx_births",
    "Lynx Deaths": "lynx_deaths",
    "Lynx Mortality": "lynx_mortality",
    "Lynx Natality": "lynx_natality",
    "Lynx": "lynx",
    "Hare": "hare",
    "Hare Births": "hare_births",
    "Hare Deaths": "prey_deaths",
    "Hare Natality": "hare_natality",
    "Wolf": "wolf",
    "Wolf Natality": 'wolf_natality',
    "Wolf Mortality": 'wolf_mortality',
    "Wolf Deaths": 'wolf_death',
    "Wolf Births": 'wolf_births',
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
    'Lynx Mortality From Hunters': "lynx_hunters_mortality",
    'Hare Mortality From Hunters': "hare_hunters_mortality",
    'Dead Wolf Density': 'dead_wolf_density',
    'Lynx Dead Wolves': 'lynx_dead_wolves'
}

__pysd_version__ = "1.4.0"

__data = {"scope": None, "time": lambda: 0}

_root = path.dirname(__file__)

x_points = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_points = [0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.005]
tck = interpolate.splrep(x_points, y_points)

x_points_wolf = [0, 12.5, 25, 37.5, 50, 62.5, 75, 82.5, 95, 107.5, 120]
y_points_wolf = [0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.005]
tck_wolf = interpolate.splrep(x_points_wolf, y_points_wolf)

def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


@cache.run
def area():
    """
    Real Name: Area
    Original Eqn: 100
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 100


@cache.run
def lynx_hunters_mortality():
    """
    Real Name: Lynx Mortality From Hunters
    Original Eqn: 0.1
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.1


@cache.run
def lynx_dead_wolves():
    """
    Real Name: Lynx_Dead_Wolves
    Original Eqn: 0.1
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.1


@cache.run
def initial_lynx_population():
    """
    Real Name: Initial Lynx Population
    Original Eqn: 125
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 125


@cache.run
def initial_hare_population():
    """
    Real Name: Initial Hare Population
    Original Eqn: 6000
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 6000

@cache.run
def initial_wolf_population():
    """
    Real Name: Initial Wolf Population
    Original Eqn: 50
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 50


@cache.step
def lynx_births():
    """
    Real Name: Lynx Births
    Original Eqn: Lynx * Lynx Natality
    Units: Lynx/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return lynx() * lynx_natality()


@cache.step
def lynx_deaths():
    """
    Real Name: Lynx Deaths
    Original Eqn: Lynx * Lynx Mortality
    Units: Lynx/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return lynx() * (lynx_mortality() + lynx_hunters_mortality()) + lynx_density() * wolf() - dead_wolf_density() * lynx_dead_wolves() * lynx()


@cache.step
def lynx_mortality():
    """
    Real Name: Lynx Mortality
    Original Eqn: Table Function
    Units: Years
    Limits: (0.005, 0.5)
    Type: component
    Subs: None


    """
    if hare_density() > 100:
        return 0.005
    elif hare_density() >= 0:
        return interpolate.splev(hare_density(), tck)
    else:
        return 0.5



@cache.run
def lynx_natality():
    """
    Real Name: Lynx Natality
    Original Eqn: 0.25
    Units: Lynx/Lynx/Year
    Limits: 0.25
    Type: constant
    Subs: None

    """
    return 0.25


@cache.step
def lynx():
    """
    Real Name: Lynx
    Original Eqn: INTEG (Lynx Births-Lynx Deaths, Initial Lynx Population)
    Units: Lynx
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return _integ_lynx()


@cache.step
def hare():
    """
    Real Name: Hare
    Original Eqn: INTEG (Hare Births-Hare Deaths, Initial Hare Population)
    Units: Hares
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return _integ_hare()


@cache.step
def hare_births():
    """
    Real Name: Hare Births
    Original Eqn: Hare * Hare Natality
    Units: Hares/Year
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return max(hare(), 0) * hare_natality()


@cache.step
def hare_deaths():
    """
    Real Name: Hare Deaths
    Original Eqn: Hare Density * Lynx
    Units: Hares/Year
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return hare_density() * lynx() + hare() * hare_hunters_mortality() + hare_density() * wolf()


@cache.step
def hare_density():
    """
    Real Name: Hare Density
    Original Eqn: Hare / Area
    Units: Hares/Square
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return hare() / area()


@cache.step
def lynx_density():
    """
    Real Name: Lynx Density
    Original Eqn: Lynx / Area
    Units: Lynxes/Square
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return lynx() / area()


def dead_wolf_density():
    """
    Real Name: Dead Wolf Density
    Original Eqn: Dead Wolf / Area
    Units: Hares/Square
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return wolf_deaths() / area()


@cache.run
def hare_natality():
    """
    Real Name: Hare Natality
    Original Eqn: 1.25
    Units: Hare/Hare/Year
    Limits: 1.25
    Type: constant
    Subs: None

    """
    return 1.25


@cache.run
def wolf_natality():
    """
    Real Name: Wolf Natality
    Original Eqn: 0.3
    Units: Lynx/Lynx/Year
    Limits: 0.3
    Type: constant
    Subs: None

    """
    return 0.3


@cache.step
def wolf_mortality():
    """
    Real Name: Wolf Mortality
    Original Eqn: Table Function
    Units: Years
    Limits: 0.5
    Type: constant
    Subs: None

    """

    if (hare_density() + lynx_density() * 5) > 125:  # one hare (4kg) = one lynx (20 kg). source: google :)
        return 0.005
    elif (hare_density() + lynx_density() * 5) >= 0:
        return interpolate.splev(hare_density() + lynx_density() * 5, tck_wolf)
    else:
        return 0.5


@cache.step
def wolf():
    """
    Real Name: Wolf
    Original Eqn: INTEG (Wolf Births-Wolf Deaths, Initial Wolf Population)
    Units: Wolf
    Limits: (0.0, None)
    Type: component
    Subs: None


    """
    return _integ_wolf()


@cache.step
def wolf_deaths():
    """
    Real Name: Wolf Deaths
    Original Eqn: Wolf * Wolf Mortality
    Units: Wolf/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return wolf() * wolf_mortality()


@cache.step
def wolf_births():
    """
    Real Name: Wolf Births
    Original Eqn: Wolf * Wolf Natality
    Units: Wolves/Year
    Limits: (None None)
    Type: component
    Subs: None


    """
    return wolf() * wolf_natality()


@cache.run
def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 50
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return 100


@cache.run
def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return 0


@cache.step
def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Year
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return time_step()


@cache.run
def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 0.0625
    Units: Year
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return 0.0625


_integ_lynx = Integ(
    lambda: lynx_births() - lynx_deaths(),
    lambda: initial_lynx_population(),
    "_integ_lynx",
)


_integ_hare = Integ(
    lambda: hare_births() - hare_deaths(),
    lambda: initial_hare_population(),
    "_integ_hare",
)

_integ_wolf = Integ(
    lambda: wolf_births() - wolf_deaths(),
    lambda: initial_wolf_population(),
    "_integ_wolf",
)
