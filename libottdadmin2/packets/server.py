from libottdadmin2.packets.registry import receive
from libottdadmin2.packets.base import ReceivingPacket, Struct
from libottdadmin2.util import gamedate_to_datetime

@receive.packet
class ServerFull(ReceivingPacket):
    packetID = 100

@receive.packet
class ServerBanned(ReceivingPacket):
    packetID = 101

@receive.packet
class ServerError(ReceivingPacket):
    packetID = 102
    format = Struct.create('B')

    def decode(self, data):
        errorcode = self.unpack(self.format, data)
        return {
            'errorcode': errorcode,
            }

@receive.packet
class ServerProtocol(ReceivingPacket):
    packetID = 103
    format = Struct.create('B')
    pre_format = Struct.create('B')
    inner_format = Struct.create('HHB')

    def decode(self, data):
        version = self.unpack(self.format, data)
        index = self.format.size
        settings = {}
        next = self.unpack(self.pre_format, data, index=index)
        index += self.pre_format.size
        while next:
            key, val, next = self.unpack(self.inner_format, data, index=index)
            index += self.inner_format.size
            settings[key] = val
        return {
            'version':      version, 
            'settings':     settings,
            }

@receive.packet
class ServerWelcome(ReceivingPacket):
    packetID = 104
    format_bool = Struct.create('B')
    format = Struct.create('IBIHH')

    def decode(self, data):
        index = 0
        name = self.unpack_str(data, index)
        index += len(name)+1
        version = self.unpack_str(data, index)
        index += len(version)+2
        dedicated = bool(self.unpack(self.format_bool, data[index-1]))
        map_name = self.unpack_str(data, index)
        index += len(map_name)+1
        seed, landscape, startyear, x, y = self.unpack(self.format, data, index)
        return {
            'name':         name,
            'version':      version,
            'dedicated':    dedicated,
            'map_name':     map_name,
            'seed':         seed,
            'landscape':    landscape,
            'startyear_orig': startyear,
            'startyear':    gamedate_to_datetime(startyear),
            'x':            x,
            'y':            y,
            }

@receive.packet
class ServerNewGame(ReceivingPacket):
    packetID = 105

@receive.packet
class ServerShutdown(ReceivingPacket):
    packetID = 106

@receive.packet
class ServerDate(ReceivingPacket):
    packetID = 107
    format = Struct.create('I')

    def decode(self, data):
        date = self.unpack(self.format, data)
        return {
            'date':         gamedate_to_datetime(date),
        }

@receive.packet
class ServerClientJoin(ReceivingPacket):
    packetID = 108
    format = Struct.create('I')

    def decode(self, data):
        clientID = self.unpack(self.format, data)
        return {
            'clientID':     clientID,
        }

@receive.packet
class ServerClientInfo(ReceivingPacket):
    packetID = 109
    format_id = Struct.create('I')
    format = Struct.create('BIB')

    def decode(self, data):
        clientID = self.unpack(self.format_id, data)
        index = self.format_id.size
        hostname = self.unpack_str(data, index)
        index += len(hostname)+1
        name = self.unpack_str(data, index)
        index += len(name)+1
        language, joindate, play_as = self.unpack(format, data, index)

        return {
            'clientID':     clientID,
            'hostname':     hostname,
            'name':         name,
            'language':     language,
            'joindate':     gamedate_to_datetime(joindate),
            'play_as':      play_as,
        }

@receive.packet
class ServerClientUpdate(ReceivingPacket):
    packetID = 110
    format_id = Struct.create('I')
    format = Struct.create('B')

    def decode(self, data):
        clientID = self.unpack(self.format_id, data)
        index = self.format_id.size
        name = self.unpack_str(data, index)
        index += len(name)+1
        play_as = self.unpack(self.format, data, index)
        return {
            'clientID':     clientID,
            'name':         name,
            'play_as':      play_as,
        }

@receive.packet
class ServerClientQuit(ServerClientJoin):
    packetID = 111

@receive.packet
class ServerClientError(ReceivingPacket):
    packetID = 112
    format = Struct.create('IB')

    def decode(self, data):
        clientID, errorcode = self.unpack(self.format, data)
        return {
            'clientID':     clientID,
            'errorcode':    errorcode,
        }

@receive.packet
class ServerCompanyNew(ReceivingPacket):
    packetID = 113
    format = Struct.create("B")

    def decode(self, data):
        companyID = self.unpack(self.format, data)
        return {
            'companyID':    companyID,
        }

@receive.packet
class ServerCompanyInfo(ReceivingPacket):
    packetID = 114
    format_id = Struct.create("B")
    format_info = Struct.create("BBIB")

    def decode(self, data):
        companyID = self.unpack(self.format_id, data)
        index = self.format_id.size
        name = self.unpack_str(data, index)
        index += len(name)+1
        manager = self.unpack_str(data, index)
        colour, passworded, startYear, isAI = self.unpack(self.format_info, data, index)
        return {
            'companyID':    companyID,
            'name':         name, 
            'manager':      manager,
            'colour':       colour,
            'passworded':   passworded,
            'startYear':    startYear,
            'isAI':         isAI
        }

@receive.packet
class ServerCompanyUpdate(ReceivingPacket):
    packetID = 115
    format_id = Struct.create("B")
    format_info = Struct.create("BBBBBBB")

    def decode(self, data):
        companyID = self.unpack(self.format_id, data)
        index = self.format_id.size
        name = self.unpack_str(data, index)
        index += len(name)+1
        manager = self.unpack_str(data, index)
        index += len(manager)+1
        colour, passworded, bankrupcyCounter, \
                s1, s2, s3, s4 = self.unpack(self.format_info, data, index)
        shares = [s1,s2,s3,s4]
        return {
            'companyID':    companyID,
            'name':         name, 
            'manager':      manager,
            'colour':       colour,
            'passworded':   passworded,
            'bankrupcyCounter': bankrupcyCounter,
            'shareholders': shares,
        }

@receive.packet
class ServerCompanyRemove(ReceivingPacket):
    packetID = 116
    format = Struct.create("BB")

    def decode(self, data):
        companyID, reason = self.unpack(self.format, data)
        return {
            'companyID':    companyID,
            'reason':       reason,
        }

@receive.packet
class ServerCompanyEconomy(ReceivingPacket):
    packetID = 117
    format = Struct.create("BQQQH")
    format_stats = Struct.create("QHH")

    def decode(self, data):
        companyID, money, currentLoan, income, \
                   delivered = self.unpack(self.format, data)
        index = self.format.size
        stats = []
        for i in range(2):
            companyValue, performanceHistory, \
                          deliveredCargo = self.unpack(self.format_stats, data, index)
            index += self.format_stats.size
            stats.append({
                'companyValue': companyValue,
                'performanceHistory': performanceHistory,
                'deliveredCargo': deliveredCargo,
                })
        return {
            'companyID':    companyID,
            'money':        money,
            'currentLoan':  currentLoan,
            'income':       income,
            'deliveredCargo': delivered,
            'history':      stats
        }

@receive.packet
class ServerCompanyStats(ReceivingPacket):
    packetID = 118
    format = Struct.create("B")
    format_stats = Struct.create("HHHHH")

    def decode(self, data):
        companyID = self.unpack(self.format, data)
        index = self.format.size
        stats = {}
        for statType in ('vehicles', 'stations'):
            train, lorry, bus, plane, ship = self.unpack(self.format_stats, data, index)
            index += self.format_stats.size
            stats[statType] = {
                'train':    train,
                'lorry':    lorry,
                'bus':      bus,
                'plane':    plane,
                'ship':     ship,
            }
        return {
            'companyID':    companyID,
            'stats':        stats,
        }

@receive.packet
class ServerChat(ReceivingPacket):
    packetID = 119
    format = Struct.create("BBI")
    format_data = Struct.create("Q")

    def decode(self, data):
        action, destType, clientID = self.unpack(self.format, data)
        index = self.format.size
        message = self.unpack_str(data, index)
        index += len(message)+1
        data = self.unpack(self.format_data, data, index)

        return {
            'action':       action,
            'destType':     destType,
            'clientID':     clientID,
            'message':      message,
            'data':         data,
        }

@receive.packet
class ServerRcon(ReceivingPacket):
    packetID = 120
    format = Struct.create("H")

    def decode(self, data):
        colour = self.unpack(self.format, data)
        index = self.format.size
        result = self.unpack_str(data, index)

        return {
            'colour':       colour,
            'result':       result,
        }

@receive.packet
class ServerConsole(ReceivingPacket):
    packetID = 121

    def decode(self, data):
        origin = self.unpack_str(data, 0)
        index = len(origin)+1
        message = self.unpack_str(data, index)
        return {
            'origin':       origin,
            'message':      message,
        }

@receive.packet
class ServerCmdNames(ReceivingPacket):
    packetID = 122

    def decode(self, data):
        pass

@receive.packet
class ServerCmdLogging(ReceivingPacket):
    packetID = 123

    def decode(self, data):
        pass 

@receive.packet
class ServerGamescript(ReceivingPacket):
    packetID = 124

    def decode(self, data):
        pass 