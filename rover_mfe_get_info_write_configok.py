from pysnmp import hlapi
from pysnmp.proto import rfc1902
import  csv,json,ipaddress




def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    print( var_bind )
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                result = str( error_status)
        except StopIteration:
            break
    return result

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                address= rfc1902.IpAddress.prettyPrint(value)
                if ipaddress.ip_address(address)  :
                    return str(address)
            except (ValueError, TypeError):
                try:
                     return str(value)
                except (ValueError, TypeError):
                  pass
    return value


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]



def set(target, value_pairs, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.setCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs(value_pairs)
    )
    return fetch(handler, 1)[0]


def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
         if type (value) == int:
               pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key),rfc1902.Integer32(value)))
         try:
             if ipaddress.ip_address(value)  :
               pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key),rfc1902.IpAddress(value)))
         except:
            if type (value) == str:
                     pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key),rfc1902.OctetString(value)))
    return pairs


def rov_mfe_tarjetas(host="",community="public"):
   return get(host,
           [
            '1.3.6.1.4.1.19324.2.2.1.3.1.1.5.1.3.1',
            '1.3.6.1.4.1.19324.2.2.1.3.1.1.5.1.3.2',
            '1.3.6.1.4.1.19324.2.2.1.3.1.1.5.1.3.3',
            '1.3.6.1.4.1.19324.2.2.1.3.1.1.5.1.3.4'
            ],
          hlapi.CommunityData(community, mpModel=0))




#######snmp version 1 es mpModel=0
#######snmp version 2c es  mpModel=1
###para los traps 1 es activado o marcado y 2 es desmarcado en la web
host = "10.8.2.73"
comunity="public"
comunity_write="private"


def rover_json():
  return  {  
        "host": "",
        "modelo": "mfe",
        "serial_number_unit" : 0,

        "slot1-tarjeta-tipo": "",
        "slot1-serial": "",
        "slot1-programa": "",
        "slot1-tipo-programa": "",
        "slot1-dtmb-channel": "",
        "slot1-asi-ip-mode": "",
        "slot1-asi-ip-asi1-addres": "",
        "slot1-asi-ip-asi2-addres": "",
        "slot1-asi-ip-asi3-addres": "",

        "slot2-tarjeta-tipo": "",
        "slot2-serial": "",
        "slot2-programa": "",  
        "slot2-tipo-programa": "",
        "slot2-dtmb-channel": "",
        "slot2-asi-ip-mode": "",
        "slot2-asi-ip-asi1-addres": "",
        "slot2-asi-ip-asi2-addres": "",
        "slot2-asi-ip-asi3-addres": "",

        "slot3-tarjeta-tipo": "",
        "slot3-serial": "",
        "slot3-programa": "",
        "slot3-tipo-programa": "",
        "slot3-dtmb-channel": "",
        "slot3-asi-ip-mode": "",
        "slot3-asi-ip-asi1-addres": "",
        "slot3-asi-ip-asi2-addres": "",
        "slot3-asi-ip-asi3-addres": "",

        "slot4-tarjeta-tipo": "",
        "slot4-serial": "",
        "slot4-programa": "",
        "slot4-tipo-programa": "",
        "slot4-dtmb-channel": "",
        "slot4-asi-ip-mode": "",
        "slot4-asi-ip-asi1-addres": "",
        "slot4-asi-ip-asi2-addres": "",
        "slot4-asi-ip-asi3-addres": "",
    }


def rovers_mfe__ASI_IP_DEC_config_trap_oid ():
    return {
    "trap asi 1 syn loss" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.1.1",
    "trap asi 1 bitrate" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.1.2",
    
    "trap asi 2 syn loss" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.2.1",
    "trap asi 2 bitrate" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.2.2",
    
    "trap asi 3 syn loss" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.3.1",
    "trap asi 3 bitrate" :  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.1.1.3.X.3.2",

     "trap eth 1 syn loss" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.1.1",
     "trap eth 1 fec" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.1.2",
     "trap eth 1 drop" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.1.3",
    

     "trap eth 2 syn loss" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.2.1",
     "trap eth 2 fec" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.2.2",
     "trap eth 2 drop" : "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.5.2.2.1.3.X.2.3",

     "umbral asi 1":  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.6.2.1.1.1.X.1",
     "umbral asi 2":  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.6.2.1.1.1.X.2",
     "umbral asi 3":  "1.3.6.1.4.1.19324.2.2.1.3.4.7.2.6.2.1.1.1.X.3"

    }

##################configuracion tarjetas ASI IP alarmas 1 es  mute 2 es envio 
rovers_mfe__ASI_IP_DEC_config_trap  = {
    "trap asi 1 syn loss": 2,
    "trap asi 1 bitrate": 2,    
    
    "trap asi 2 syn loss": 2,
    "trap asi 2 bitrate": 2,
    
    "trap asi 3 syn loss": 2,
    "trap asi 3 bitrate": 2,
    
    "trap eth 1 syn loss" :2 ,
    "trap eth 1 fec" : 2,
      "trap eth 1 drop" : 2,

    
    "trap eth 2 syn loss" :2,
    "trap eth 2 fec" : 2,
      "trap eth 2 drop" : 2,

     "umbral asi 1":  17980, #umbral de la salida asi1 para trap de bitrate
     "umbral asi 2":  17980, #umbral de la salida asi1 para trap de bitrate
     "umbral asi 3":  17980   # telecentro   umbral de la salida asi1 para trap de bitrate
    
    }

###     TOCAR  +######config oid trap de la unit#######################################
rovers_mfe__manager_config_trap ={
     "manager_create":  5, #valor 4 indica create
    "manager_ip" :  "172.8.1.20",  # tipo strinfg ip
    "manager_port" :  "9000",  # tipo string puerto
    "manager_time":  -1   # valor -1 indica persistente snmp
   
    }
###    NO TOCAR  +######config oid trap de la unit#######################################
def rovers_mfe__manager_config_trap_oid ():
    return {
     "manager_create":  "1.3.6.1.4.1.19324.2.2.1.3.1.2.5.5.1.1.5.1",
    "manager_ip" :  "1.3.6.1.4.1.19324.2.2.1.3.1.2.5.5.1.1.2.1",
    "manager_port" :  "1.3.6.1.4.1.19324.2.2.1.3.1.2.5.5.1.1.3.1",
    "manager_time":  "1.3.6.1.4.1.19324.2.2.1.3.1.2.5.5.1.1.4.1"
   
    }
##################configuracion tarjetasDTMB CUBA alarmas 1 es  mute 2 es envio 
rovers_mfe__DTMB_CUBA_config_trap = {
    "trap unlock": 2,
    "trap power level": 2,
    "trap mer": 2,
    "trap ber": 2
    }
###    NO TOCAR  +######config oid trap de tarjetas mpeg decoder#######################################
def rovers_mfe__DTMB_CUBA_config_trap_oid ():
    return {
    "trap unlock" :  "1.3.6.1.4.1.19324.2.2.1.3.2.2.2.4.1.3.X.1",
    "trap power level" :  "1.3.6.1.4.1.19324.2.2.1.3.2.2.2.4.1.3.X.2",
    "trap mer":  "1.3.6.1.4.1.19324.2.2.1.3.2.2.2.4.1.3.X.3",
    "trap ber":  "1.3.6.1.4.1.19324.2.2.1.3.2.2.2.4.1.3.X.4"
    

    }
##################configuracion tarjetas ASI SWITCH alarmas 1 es  mute 2 es envio 
rovers_mfe__asi_switch_config_trap = {
    "syncLoss": 2,
    "patLoss": 2,
    "transportStreamId": 2,
    "networkId": 2,
    "stuffingRate": 2
    }
###    NO TOCAR  +######config oid trap de tarjetas ASI SWITCH#######################################
def rovers_mfe__asi_switch_config_trap_oid ():
    return {
     "syncLoss": "1.3.6.1.4.1.19324.2.2.1.3.4.2.2.3.1.3.X.1",
    "patLoss": "1.3.6.1.4.1.19324.2.2.1.3.4.2.2.3.1.3.X.2",
    "transportStreamId": "1.3.6.1.4.1.19324.2.2.1.3.4.2.2.3.1.3.X.3",
    "networkId": "1.3.6.1.4.1.19324.2.2.1.3.4.2.2.3.1.3.X.4",
    "stuffingRate": "1.3.6.1.4.1.19324.2.2.1.3.4.2.2.3.1.3.X.5"

    }
##################configuracion tarjetas satelital alarmas 1 es  mute 2 es envio 
rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap = {
    "trap unlock": 2,
    "trap power level": 2,
    "trap snr": 2,
    "trap ber": 2,
    "trap lnb": 2
    }
###    NO TOCAR  +######config oid trap de tarjetas satelital#######################################
def rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap_oid ():
    return {
    "trap unlock" :  "1.3.6.1.4.1.19324.2.2.1.3.2.1.2.6.1.3.X.1",
    "trap power level" :  "1.3.6.1.4.1.19324.2.2.1.3.2.1.2.6.1.3.X.2",
    "trap snr":  "1.3.6.1.4.1.19324.2.2.1.3.2.1.2.6.1.3.X.3",
    "trap ber":  "1.3.6.1.4.1.19324.2.2.1.3.2.1.2.6.1.3.X.4",
    "trap lnb":  "1.3.6.1.4.1.19324.2.2.1.3.2.1.2.6.1.3.X.5"

    }
#########################################################
###tarjetas MPEG DECODER TV CAMBIAR ##########configuracion tarjetas mpeg decoder TRAPS 1 es  mute 2 es envio 
rovers_mfe__mpeg_decoder_config_trap_tv = {
    "trap no asi": 2,
    "trap no video": 2,
    "trap ts changed": 1,
    "trap no audio": 2,
    "trap encrypted": 1,
    "trap black": 1,
    "trap still": 1
    }


#########################################################
###tarjetas MPEG DECODER Radio CAMBIAR ##########configuracion tarjetas mpeg decoder TRAPS 1 es  mute 2 es envio 
rovers_mfe__mpeg_decoder_config_trap_radio = {
    "trap no asi": 2,
    "trap no video": 1,
    "trap ts changed": 1,
    "trap no audio": 2,
    "trap encrypted": 1,
    "trap black": 1,
    "trap still": 1
    }
###    NO TOCAR  +######config oid trap de tarjetas mpeg decoder#######################################
def rovers_mfe__mpeg_decoder_config_trap_oid ():
    return {
    "trap no asi":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.1",
    "trap no video":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.2",
    "trap ts changed":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.3",
    "trap no audio":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.4",
    "trap encrypted":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.5",
    "trap black":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.6",
    "trap still":  "1.3.6.1.4.1.19324.2.2.1.3.3.1.2.2.1.3.X.7"
    }
########  NO TOCAR  #####significado de traps ##1 es mute 2 es envio#######################################
rovers_mfe__mpeg_decoder_config_trap_oid_significado = ["","mute", " envio"]

def create_csv_file():
    with open('rovers_mfe_programas.csv', 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(rover_json())

create_csv_file()
     
def rovers_mfe_config_mpeg_decoder_traps(host, json = rover_json () ):
 
 rover_json=json 
 #conectao con el roversa
 print ("HOST: "  + host)
 ##valido que es un runit de rover check rover mef v2 .1.3.6.1.4.1.19324.2.2.1.3.1.1.1.0  = 2
 resultado_snmp_get = get(host, [ "1.3.6.1.4.1.19324.2.2.1.3.1.1.1.0" ] , hlapi.CommunityData(comunity))
 if  resultado_snmp_get == "0":
     return 
 print (  "mfe802v2(2) ES VALOR 2: --> "  +" : "+ str(resultado_snmp_get[ "1.3.6.1.4.1.19324.2.2.1.3.1.1.1.0"])  )
 if  resultado_snmp_get[ "1.3.6.1.4.1.19324.2.2.1.3.1.1.1.0"]  != 2 :
     return 

 
 
 print ("check splunk ip manager")

 
 ### fijar las prpiedades del manager
 oid=[]
 myoid_manager= rovers_mfe__manager_config_trap_oid ()
 
 for llave_manager in myoid_manager:
         print ( "WRITE " + llave_manager )
         if "0" == set( host , { myoid_manager [ llave_manager ] : rovers_mfe__manager_config_trap[llave_manager] }, hlapi.CommunityData( comunity_write, mpModel=0 )):
             return

 ### fijar las prpiedades del manager
 myoid_manager= rovers_mfe__manager_config_trap_oid ()
 for llave_manager in myoid_manager:
                oid.append( myoid_manager  [llave_manager] )
 resultado_snmp_get = get(host, oid , hlapi.CommunityData(comunity))

 for llave in  resultado_snmp_get:   
     print (  llave  +" : "+ str(resultado_snmp_get[llave])  )
 
 rover_json[ "host"]= host
 
 #get serial numer
 oid = ["1.3.6.1.4.1.19324.2.2.1.3.1.1.3.0"]
 resultado_snmp_get = get(host,oid, hlapi.CommunityData(comunity))
 for llave in resultado_snmp_get:
     print ("unit serial number: " + llave +" : "+ str(resultado_snmp_get[llave]))
 rover_json[ "serial_number_unit"]= str(resultado_snmp_get[llave])
 tarjetas = rov_mfe_tarjetas(host,comunity)
 slot =1
 if tarjetas != str(0):
  for value in tarjetas:
     ###inprime tipo de tarjeta
     print("slot> " + str(slot) + " " + tarjetas[value]  )
     ###define tipo de tarjeta mpeg, asi-ip etc
     rover_json[ "slot" + str(slot) + "-tarjeta-tipo"]= tarjetas[value]

     ## Trajeta ASI SWITCH DE 2 ASIS
     if tarjetas[value] =="ASI PROCESSOR":
           ##get serial number en este caso serial ID number
           oid_sn="1.3.6.1.4.1.19324.2.2.1.3.4.2.1.1.5." + str(slot)
           sendm_get_sn = get(host, [ oid_sn ] , hlapi.CommunityData(comunity))
           for value_sn in  sendm_get_sn:
                print("Tarjeta serial:" + str( sendm_get_sn[value_sn])   )
                rover_json[ "slot" + str(slot) + "-serial"]= str( sendm_get_sn[value_sn])

           ### obtener estado de los traps
           oid=[]
           myoid= rovers_mfe__asi_switch_config_trap_oid ()

           for llave in myoid:
                oid.append(myoid[llave].replace("X",str(slot)))
           resultado_snmp_get = get(host, oid , hlapi.CommunityData(comunity))
           #print(resultado_snmp_get)

           myoid= rovers_mfe__asi_switch_config_trap_oid ()
           for llave in resultado_snmp_get:
                for name in myoid:
                    if myoid[name].replace("X",str(slot)) == llave:
                         #imprime estado de mute de envio de traps y estado mute o envio
                         print( name +    " --- " + str(resultado_snmp_get[llave]) +  " oid: "+ llave)
                         ##corregir el error de configuracion
                         if rovers_mfe__asi_switch_config_trap[name] != resultado_snmp_get[llave]:
                                 print ("hay que corregir tarjeta asi switch")
                                 set( host , {llave: rovers_mfe__asi_switch_config_trap[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))
                                 import time
                                 time.sleep( 5 )
         
     
     ## Tarjta ASI-IP DECAPSULADORA
     if tarjetas[value] =="ASI <-> IP Gateway":
           ##get serial number en este caso serial id
           oid_sn="1.3.6.1.4.1.19324.2.2.1.3.4.7.1.1.5." + str(slot)
           sendm_get_sn = get(host, [ oid_sn ] , hlapi.CommunityData(comunity))
           for value_sn in  sendm_get_sn:
                print("Tarjeta serial:" + str( sendm_get_sn[value_sn])   )
                rover_json[ "slot" + str(slot) + "-serial"]= str( sendm_get_sn[value_sn])
           #### get operation mode encapsulation o decapsulator
           oid_op_mode="1.3.6.1.4.1.19324.2.2.1.3.4.7.2.2.1.1.1." + str(slot)
           sendm_get_op_mode = get(host, [  oid_op_mode] , hlapi.CommunityData(comunity))
           for value_op_mode in  sendm_get_op_mode:
                ##MODO DECAPSDUALDOR
                if sendm_get_op_mode[value_op_mode] == 1 :
                      print("Operation Mode ASI-IP : Decapsulador"  )
                      rover_json[ "slot" + str(slot) + "-asi-ip-mode"]= "Decapsulador"
                      ## gest direccion para saber si es sd o hd
                      oid_asi_ip_address=["1.3.6.1.4.1.19324.2.2.1.3.4.7.2.4.1.1." + str(slot )+ ".1","1.3.6.1.4.1.19324.2.2.1.3.4.7.2.4.1.1." + str(slot )+ ".2","1.3.6.1.4.1.19324.2.2.1.3.4.7.2.4.1.1." + str(slot )+ ".3" ]
                      sendm_get_asi_ip_address = get(host, oid_asi_ip_address , hlapi.CommunityData(comunity))
                      asi = 1
                      for value_asi_ip_address in  sendm_get_asi_ip_address:
                           print("ASI " +  str(asi) + " >>" + str( sendm_get_asi_ip_address [ value_asi_ip_address  ] )   )
                           rover_json[ "slot" + str(slot) + "-asi-ip-asi"+ str(asi) + "-addres"] = str( sendm_get_asi_ip_address [ value_asi_ip_address  ] )
                           asi += 1
                      ## leer estado de los trap asi
                      oid_asi_ip=[]
                      xx_asi_ip = rovers_mfe__ASI_IP_DEC_config_trap_oid ()
                      for xx_oid_asi_ip in   xx_asi_ip :
                         oid_asi_ip.append( xx_asi_ip [ xx_oid_asi_ip  ].replace("X", str(slot)))
                         
                      resultado_snmp_get = get(host, oid_asi_ip , hlapi.CommunityData(comunity))
                      #print(resultado_snmp_get)

                      myoid= rovers_mfe__ASI_IP_DEC_config_trap_oid ()
                      for llave in resultado_snmp_get:
                           for name in myoid:
                                if myoid[name].replace("X",str(slot)) == llave:
                                     #imprime estado de mute de envio de traps y estado mute o envio
                                      print( name +    " --- " + str(resultado_snmp_get[llave]) +  " oid: "+ llave)
                                      ##corregir el error de configuracion
                                      if rovers_mfe__ASI_IP_DEC_config_trap[name] != resultado_snmp_get[llave]:
                                          print ("hay que corregir tarjeta satelite")
                                          set( host , {llave: rovers_mfe__ASI_IP_DEC_config_trap[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))

                         

                else :
                      print("Operation Mode ASI-IP : Encapsulador"  )
                      rover_json[ "slot" + str(slot) + "-asi-ip-mode"]= "Encapsulador"

     
     ## Trajeta 
     if tarjetas[value] =="DTMB CUBA":
           ##get serial number
           oid_sn="1.3.6.1.4.1.19324.2.2.1.3.2.2.1.1.4." + str(slot)
           sendm_get_sn = get(host, [ oid_sn ] , hlapi.CommunityData(comunity))
           for value_sn in  sendm_get_sn:
                print("Tarjeta serial:" + str( sendm_get_sn[value_sn])   )
                rover_json[ "slot" + str(slot) + "-serial"]= str( sendm_get_sn[value_sn])
           ##obtener_canal_sintonizado
           oid_ch="1.3.6.1.4.1.19324.2.2.1.3.2.2.2.1.1.1." + str(slot)
           sendm_get_ch = get(host, [ oid_ch ] , hlapi.CommunityData(comunity))
           for value_ch in  sendm_get_ch:
                print("Tarjeta DTMB :" + str( sendm_get_ch[value_ch])   )
                rover_json[ "slot" + str(slot) + "-dtmb-channel"]= str( sendm_get_ch[value_ch])


           ### obtener estado de los traps
           oid=[]
           myoid= rovers_mfe__DTMB_CUBA_config_trap_oid ()
          
           for llave in myoid:
                oid.append(myoid[llave].replace("X",str(slot)))
           resultado_snmp_get = get(host, oid , hlapi.CommunityData(comunity))
           #print(resultado_snmp_get)

           myoid= rovers_mfe__DTMB_CUBA_config_trap_oid ()
           for llave in resultado_snmp_get:
                for name in myoid:
                    if myoid[name].replace("X",str(slot)) == llave:
                         #imprime estado de mute de envio de traps y estado mute o envio
                         print( name +    " --- " + str(resultado_snmp_get[llave]) +  " oid: "+ llave)
                         ##corregir el error de configuracion
                         if rovers_mfe__DTMB_CUBA_config_trap[name] != resultado_snmp_get[llave]:
                                 print ("hay que corregir tarjeta satelite")
                                 set( host , {llave: rovers_mfe__DTMB_CUBA_config_trap[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))


             
     ## Trajeta Satelite
     if tarjetas[value] =="DVB-S/DVB-S2 32APSK":
           ##get serial number
           oid_sn="1.3.6.1.4.1.19324.2.2.1.3.2.1.1.1.4." + str(slot)
           sendm_get_sn = get(host, [ oid_sn ] , hlapi.CommunityData(comunity))
           for value_sn in  sendm_get_sn:
                print("Tarjeta serial:" + str( sendm_get_sn[value_sn])   )
                rover_json[ "slot" + str(slot) + "-serial"]= str( sendm_get_sn[value_sn])
           ### obtener estado de los traps 
           oid=[]
           myoid= rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap_oid ()
          
           for llave in myoid:
                oid.append(myoid[llave].replace("X",str(slot)))
           resultado_snmp_get = get(host, oid , hlapi.CommunityData(comunity))
           
           
           myoid= rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap_oid ()
           for llave in resultado_snmp_get:
                for name in myoid:
                    if myoid[name].replace("X",str(slot)) == llave:
                         #imprime estado de mute de envio de traps y estado mute o envio
                         print( name +    " --- " + str(resultado_snmp_get[llave]) +  " oid: "+ llave)
                         ##corregir el error de configuracion
                         if rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap[name] != resultado_snmp_get[llave]:
                                 print ("hay que corregir tarjeta satelite")
                                 set( host , {llave: rovers_mfe__DVB_S_DVB_S2_32APSK_config_trap[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))




                
     ## Tarjta Mpeg decoder 
     if tarjetas[value] == "MPEG4 Decoder":          
           ##get serial number
           oid_sn="1.3.6.1.4.1.19324.2.2.1.3.3.1.1.1.4." + str(slot)
           sendm_get_sn = get(host, [ oid_sn ] , hlapi.CommunityData(comunity))
           for value_sn in  sendm_get_sn:
                print("Tarjeta serial:" + str( sendm_get_sn[value_sn])   )
                rover_json[ "slot" + str(slot) + "-serial"]= str( sendm_get_sn[value_sn])
           ##
           oid_programa_id="1.3.6.1.4.1.19324.2.2.1.3.3.1.2.1.1.2." + str(slot)
           programa_id = get(host,[ oid_programa_id ], hlapi.CommunityData(comunity))
           for value_programa in programa_id:
                print("Programa ID:" + str(programa_id[value_programa])   )
           
           oid_programa_name=".1.3.6.1.4.1.19324.2.2.1.3.3.1.3.1.1.2." + str(slot)+"."+ str(programa_id[value_programa])
           programa_name = get(host,[ oid_programa_name ], hlapi.CommunityData(comunity))
           for value_name in programa_name:
                print("Programa name:" + str(programa_name[value_name])   )
           
           rover_json[ "slot" + str(slot) + "-programa"]= str(programa_name[value_name]).replace("á","a").replace("é","e").replace("í","i").replace("ó","o")
          
           # obtener estado de los traps 
           oid=[]
           myoid= rovers_mfe__mpeg_decoder_config_trap_oid ()
          
           for llave in myoid:
                oid.append(myoid[llave].replace("X",str(slot)))
           resultado_snmp_get = get(host, oid , hlapi.CommunityData(comunity))
           
           myoid= rovers_mfe__mpeg_decoder_config_trap_oid ()
           for llave in resultado_snmp_get:
                
                for name in myoid:
                    if myoid[name].replace("X",str(slot)) == llave:
                         #imprime estado de mute de envio de traps y estado mute o envio
                         print(name   +  ":  "+ rovers_mfe__mpeg_decoder_config_trap_oid_significado[resultado_snmp_get[llave]]  + " --- " + str(resultado_snmp_get[llave]) +  " oid: "+ llave)
                         ##corregir el error de configuracion
                         if programa_id[value_programa] > 8 :
                              #print ("Programa de Radio")
                              rover_json[ "slot" + str(slot) + "-tipo-programa"]= "radio"
                              if rovers_mfe__mpeg_decoder_config_trap_radio[name] != resultado_snmp_get[llave]:
                                 print ("hay que corregir tarjeta radio")
                                 set( host , {llave: rovers_mfe__mpeg_decoder_config_trap_radio[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))
                         else:
                              #print ("Programa de Television")
                              rover_json[ "slot" + str(slot) + "-tipo-programa"]= "tv"
                              if rovers_mfe__mpeg_decoder_config_trap_tv[name] != resultado_snmp_get[llave]:
                                 print ("hay que corregir tarjeta television")
                                 set( host , {llave: rovers_mfe__mpeg_decoder_config_trap_tv[name] }, hlapi.CommunityData( comunity_write, mpModel=0 ))
     slot = slot + 1
 with open('rovers_mfe_programas.csv', 'at', newline='\n') as csvfile:
     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
     spamwriter.writerow(rover_json.values())
     print (" ")




##########################################################
##########################################################
file = 'rover_mfe_ip.csv'


with open( file , 'r', newline='\n') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         try : 
               if ipaddress.IPv4Address( str(row ["host"]) ).version == 4  :
                     print ( "Rover: " + str(row ["host"]) )
                     rovers_mfe_config_mpeg_decoder_traps( str(row ["host"]), rover_json() )
         except :
                print ( "<" +  row ["host"] + ">")



   
print(" cambio el asi  bitrate del telecentro")


