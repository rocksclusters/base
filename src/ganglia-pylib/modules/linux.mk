CC = gcc
CCOPTS = -fPIC
OSVERSION = $(shell lsb_release -rs | cut -f 1 -d .)
