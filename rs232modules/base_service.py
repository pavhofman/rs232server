#!/usr/bin/env python2

# Copyright (C) 2011,2012,2013 Brendan Le Foll <brendan@fridu.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import logging
import serial
import Shared
from SerialController import SerialController

class BaseService(dbus.service.Object):

  def __init__(self, bus_name, obj_path, tty, baud_rate, readval, cmds):
    dbus.service.Object.__init__(self, bus_name, obj_path)
    self.logger = logging.getLogger(Shared.APP_NAME + '.' + self.__class__.__name__ )
    self.cmds = cmds
    try:
      # expecting typical 8n1 case
      ser = serial.Serial(tty, baud_rate, timeout=Shared.DELAY, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    except:
      raise invalidtty("Could not open " + tty)

    self.queue = SerialController(ser, readval)
    self.logger.debug("Started service on %s", obj_path)

  def help(self):
    string = ""
    for p in self.cmds.commands:
      string += '\n' + p
    # strip first character
    return string[1:]

  def send_cmd(self, cmd, repeat, check):
    return NotImplemented

  def clear(self):
    return NotImplemented