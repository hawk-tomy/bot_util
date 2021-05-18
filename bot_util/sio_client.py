from asyncio import Queue
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path


from socketio import AsyncClient
import yaml


from .config import ConfigBase, config


__all__ = ('SioClient',)
logger = getLogger(__name__)


@dataclass
class SocketIOSettings(ConfigBase):
    name: str= ''
    password: str= ''
    url: str= ''
config.add_default_config(SocketIOSettings, key='socketio_settings')
sio_setting: SocketIOSettings= config.socketio_settings
url = sio_setting.url

class SioClient(AsyncClient):
    def __init__(self):
        super().__init__(
            logger=logger.getChild('sIO'),
            engineio_logger=logger.getChild('eIO'),
        )

        #4 sIO p2b event
        self.__event_dict: dict[str, Queue]= {}
        #4 sIO b2P event
        self.__wait_events: dict[int, Queue]= {}
        self.__latest_id: int= 0

        event_dict_path = Path(__file__).resolve().parent / 'event_dict.yaml'
        if event_dict_path.exists():
            with event_dict_path.open(encoding='utf-8')as f:
                self.event_dict: dict[str, str]= yaml.safe_load(f)
        else:
            self.event_dict = {}
            with event_dict_path.open(encoding='utf-8', mode='w')as f:
                yaml.dump(self.event_dict,f)
        self.__loader()
        self.__events_register()

    #data framework
    def __loader(self):
        for event, type_ in self.event_dict.items():
            if type_ == 'p2b':
                self._p2b_handler(event, self.add_p2b_event(event))
            elif type_ == 'b2p':
                self._b2p_handler(event)
            else:
                raise ValueError(f'this event {event} is not found')

    def _p2b_handler(self, event: str, queue: Queue):
        @self.on(event)
        async def decorator(json):
            logger.debug(json)
            await queue.put(json)

    def _b2p_handler(self, event: str):
        @self.on(event)
        async def decorator(json: dict):
            logger.debug(json)
            id_ = json.get('id_')
            if self.is_b2p_id_in(id_):
                await self.get_b2p_data_by_id(id_).put(json)

    def add_p2b_event(self, event: str)-> Queue:
        queue = Queue()
        self.__event_dict[event] = queue
        return queue

    def get_p2b_events(self)-> list[str]:
        return list(self.__event_dict.keys())

    def get_p2b_event_queue(self, event: str)-> Queue:
        return self.__event_dict.get(event)

    def add_b2p_event(self)-> tuple[int, Queue]:
        self.__latest_id += 1
        queue = Queue()
        self.__wait_events[self.__latest_id] = queue
        return self.__latest_id, queue

    def get_b2p_data_by_id(self, id_: int)-> Queue:
        return self.__wait_events.pop(id_)

    def is_b2p_id_in(self, id_: int)-> bool:
        return id_ in self.__wait_events

    #hard coding events
    def __events_register(self):
        @self.event
        async def login(json):
            logger.info(json)
            await self.sleep(1)
            await self.emit(
                'login',
                {'name': sio_setting.name,'password': sio_setting.password,}
            )

        @self.event
        async def login_result(json):
            logger.info(json)
            if json.pop('status') != 'success':
                logger.info('login is failed')
                await self.disconnect()
            else:
                logger.info('login is success')
                await self.emit('get_notice')

        @self.event
        async def get_notice(json):
            notice = json['notices']
            not_notices = {
                'PTsiege_plugin','PTlobby_plugin','PTPVP_plugin','PTRPG_plugin',
                'PTNuma_plugin','STlobby_plugin','test_plugin','test1_plugin',
                'test2_plugin','test3_plugin'
                } - set(notice)
            for not_notice in not_notices:
                await self.emit('notice',{'name':not_notice})

        @self.event
        async def notice(json):
            logger.info(f'{json["status"]} : {json["message"]}')

        @self.event
        async def connect():
            logger.info('connected to server')

        @self.event
        async def disconnect():
            logger.info('disconnected from server')

        @self.event
        async def message(msg):
            logger.info(msg)

    #run
    async def run(self):
        await self.connect(
            config.socketio_settings.url,
            transports='websocket'
        )
