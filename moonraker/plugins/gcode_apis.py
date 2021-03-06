# Map HTTP/Websocket APIs for specific gcode tasks
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

GCODE_ENDPOINT = "gcode/script"

class GCodeAPIs:
    def __init__(self, server):
        self.server = server

        # Register GCode Endpoints
        self.server.register_endpoint(
            "/printer/print/pause", "printer_print_pause", ['POST'],
            self.gcode_pause)
        self.server.register_endpoint(
            "/printer/print/resume", "printer_print_resume", ['POST'],
            self.gcode_resume)
        self.server.register_endpoint(
            "/printer/print/cancel", "printer_print_cancel", ['POST'],
            self.gcode_cancel)
        self.server.register_endpoint(
            "/printer/print/start", "printer_print_start", ['POST'],
            self.gcode_start_print)
        self.server.register_endpoint(
            "/printer/restart", "printer_restart", ['POST'],
            self.gcode_restart)
        self.server.register_endpoint(
            "/printer/firmware_restart", "printer_firmware_restart", ['POST'],
            self.gcode_firmware_restart)

    async def _send_gcode(self, script):
        args = {'script': script}
        request = self.server.make_request(
            GCODE_ENDPOINT, 'POST', args)
        result = await request.wait()
        if isinstance(result, self.server.error):
            raise result
        return result

    async def gcode_pause(self, path, method, args):
        return await self._send_gcode("PAUSE")

    async def gcode_resume(self, path, method, args):
        return await self._send_gcode("RESUME")

    async def gcode_cancel(self, path, method, args):
        return await self._send_gcode("CANCEL_PRINT")

    async def gcode_start_print(self, path, method, args):
        filename = args.get('filename')
        # XXX - validate that file is on disk

        if filename[0] != '/':
            filename = '/' + filename
        script = "M23 " + filename + "\nM24"
        return await self._send_gcode(script)

    async def gcode_restart(self, path, method, args):
        return await self._send_gcode("RESTART")

    async def gcode_firmware_restart(self, path, method, args):
        return await self._send_gcode("FIRMWARE_RESTART")

def load_plugin(server):
    return GCodeAPIs(server)
