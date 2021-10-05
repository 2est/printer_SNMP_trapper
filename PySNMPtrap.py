# import selection
from time import strftime
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import socket

# create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# getting external local ip address and declaration port
TrapAgentAddress = socket.gethostbyname(socket.gethostname())
Port = 162

# create local MIB`s dict
dictionary = dict()
dictionary = {'1.3.6.1.2.1.1.3.0': {'0': 'sysUpTimeInstance'},
              '1.3.6.1.6.3.1.1.4.1.0': {'0': 'snmpTrapOID'},
              '1.3.6.1.6.3.18.1.3.0': {'0': 'snmpTrapAddress'},
              '1.3.6.1.6.3.18.1.4.0': {'0': 'snmpTrapCommunity'},
              '1.3.6.1.6.3.1.1.4.3.0': {'0': 'snmpTrapEnterprise'},
              '1.3.6.1.2.1.43.18.1.1.2.1': {'0': 'prtAlertSeverityLevel',
                                            '1': 'other',
                                            '3': 'critical',
                                            '4': 'warning'
                                            },
              '1.3.6.1.2.1.43.18.1.1.3.1': {'0': 'prtAlertTrainingLevel',
                                            '1': 'other',
                                            '2': 'unknown',
                                            '3': 'untrained',
                                            '4': 'training',
                                            '5': 'fieldService',
                                            '6': 'management'
                                            },
              '1.3.6.1.2.1.43.18.1.1.4.1': {'0': 'prtAlertGroup',
                                            '3': 'hostResourcesMIBStorageTable',
                                            '4': 'hostResourcesMIBDeviceTable',
                                            '5': 'generalPrinter',
                                            '6': 'cover',
                                            '7': 'localization',
                                            '8': 'input',
                                            '9': 'output',
                                            '10': 'marker',
                                            '11': 'markerSupplies',
                                            '12': 'markerColorant',
                                            '13': 'mediaPath',
                                            '14': 'channel',
                                            '15': 'interpreter',
                                            '16': 'consoleDisplayBuffer',
                                            '17': 'consoleLights'
                                            },
              '1.3.6.1.2.1.43.18.1.1.5.1': {'0': 'prtAlertGroupIndex'},
              '1.3.6.1.2.1.43.18.1.1.6.1': {'0': 'prtAlertLocation'},
              '1.3.6.1.2.1.43.18.1.1.7.1': {'0': 'prtAlertCode',
                                            '1': 'other',
                                            '2': 'unknown',
                                            '3': 'coverOpen',
                                            '4': 'coverClosed',
                                            '5': 'interlockOpen',
                                            '6': 'interlockOpenClosed',
                                            '7': 'configurationChange',
                                            '8': 'jam',
                                            '9': 'subunitMissing',
                                            '10': 'subunitLifeAlmostOver',
                                            '11': 'subunitLifeOver',
                                            '12': 'subunitAlmostEmpty',
                                            '13': 'subunitEmpty',
                                            '14': 'subunitAlmostFull',
                                            '15': 'subunitFull',
                                            '16': 'subunitNearLimit',
                                            '17': 'subunitAtLimit',
                                            '18': 'subunitOpened',
                                            '19': 'subunitClosed',
                                            '20': 'subunitTurnedOn',
                                            '21': 'subunitTurnedOff',
                                            '22': 'subunitOffline',
                                            '23': 'subunitPowerSaver',
                                            '24': 'subunitWarmingUp',
                                            '25': 'subunitAdded',
                                            '26': 'subunitRemoved',
                                            '27': 'subunitResourceAdded',
                                            '28': 'subunitResourceRemoved',
                                            '29': 'subunitRecoverableFailure',
                                            '30': 'subunitUnrecoverableFailure',
                                            '31': 'subunitRecoverableStorageError',
                                            '32': 'subunitUnrecoverableStorageError',
                                            '33': 'subunitMotorFailure',
                                            '34': 'subunitMemoryExhausted',
                                            '35': 'subunitUnderTemperature',
                                            '36': 'subunitOverTemperature',
                                            '37': 'subunitTimingFailure',
                                            '38': 'subunitThermistorFailure',
                                            '501': 'doorOpen',
                                            '502': 'doorClosed',
                                            '503': 'powerUp',
                                            '504': 'powerDown',
                                            '505': 'printerNMSReset',
                                            '506': 'printerManualReset',
                                            '507': 'printerReadyToPrint',
                                            '801': 'inputMediaTrayMissing',
                                            '802': 'inputMediaSizeChange',
                                            '803': 'inputMediaWeightChange',
                                            '804': 'inputMediaTypeChange',
                                            '805': 'inputMediaColorChange',
                                            '806': 'inputMediaFormPartsChange',
                                            '807': 'inputMediaSupplyLow',
                                            '808': 'inputMediaSupplyEmpty',
                                            '809': 'inputMediaChangeRequest',
                                            '810': 'inputManualInputRequest',
                                            '811': 'inputTrayPositionFailure',
                                            '812': 'inputTrayElevationFailure',
                                            '813': 'inputCannotFeedSizeSelected',
                                            '901': 'outputMediaTrayMissing',
                                            '902': 'outputMediaTrayAlmostFull',
                                            '903': 'outputMediaTrayFull',
                                            '904': 'outputMailboxSelectFailure',
                                            '1001': 'markerFuserUnderTemperature',
                                            '1002': 'markerFuserOverTemperature',
                                            '1003': 'markerFuserTimingFailure',
                                            '1004': 'markerFuserThermistorFailure',
                                            '1005': 'markerAdjustingPrintQuality',
                                            '1102': 'markerInkEmpty',
                                            '1103': 'markerPrintRibbonEmpty',
                                            '1104': 'markerTonerAlmostEmpty',
                                            '1105': 'markerInkAlmostEmpty',
                                            '1106': 'markerPrintRibbonAlmostEmpty',
                                            '1107': 'markerWasteTonerReceptacleAlmostFull',
                                            '1108': 'markerWasteInkReceptacleAlmostFull',
                                            '1109': 'markerWasteTonerReceptacleFull',
                                            '1110': 'markerWasteInkReceptacleFull',
                                            '1111': 'markerOpcLifeAlmostOver',
                                            '1112': 'markerOpcLifeOver',
                                            '1113': 'markerDeveloperAlmostEmpty',
                                            '1114': 'markerDeveloperEmpty',
                                            '1115': 'markerTonerCartridgeMissing',
                                            '1301': 'mediaPathMediaTrayMissing',
                                            '1302': 'mediaPathMediaTrayAlmostFull',
                                            '1303': 'mediaPathMediaTrayFull',
                                            '1304': 'mediaPathCannotDuplexMediaSelected',
                                            '1501': 'interpreterMemoryIncrease',
                                            '1502': 'InterpreterMemoryDecrease',
                                            '1503': 'InterpreterCartridgeAdded',
                                            '1504': 'InterpreterCartridgeDeleted',
                                            '1505': 'InterpreterResourceAdded',
                                            '1506': 'InterpreterResourceDecrease',
                                            '1507': 'InterpreterResourceUnavailable',
                                            '1509': 'InterpreterComplexPageEncountered',
                                            '1801': 'alertRemovalOfBinaryChangeEntry'
                                            },
              '1.3.6.1.2.1.43.18.1.1.8.1': {'0': 'prtAlertDescription'},
              '1.3.6.1.2.1.43.18.1.1.9.1': {'0': 'prtAlertTime'}
              }

# setup UDP over IPv4 transport endpoint
config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
)

# Configure community here
config.addV1System(snmpEngine, 'my-area', 'public')


# definition section
# Write log of traps in *.txt file, with date in name
def wrLog(text):
    date = 'received_traps' + strftime('%Y%m%d') + '.log'
    with open(date, 'a') as log:
        log.write(text + '\n')


# create post format for log
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    wrLog('\n Received new Trap message ' + strftime('%Y-%m-%d_%H:%M:%S'))
    for name, value in varBinds:
        n, v = (encript(name, value))
        wrLog('%s = %s' % (n, v))


# encrypting traps
def encript(OIDs, values):
    name = str(OIDs)
    val = str(values.prettyPrint())
    for i in dictionary:
        b = str(i)
        if name.startswith(b):
            name = dictionary[b]['0']
            for k in dictionary[b]:
                if k == val and k != '0':
                    val = dictionary[b][val]
    return name, val


wrLog(f'Agent is listening SNMP Trap on {TrapAgentAddress}, Port: {Port}')

ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise


