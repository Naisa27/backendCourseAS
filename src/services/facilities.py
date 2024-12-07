from src.exceptions import ObjectNotFoundException, FacilitiesNotFoundException
from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiyService(BaseService):
    async def add_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add( data )
        await self.db.commit()

        test_task.delay( 5 )
        return facility

    async def get_facilities( self ):
        try:
            return await self.db.facilities.get_all()
        except ObjectNotFoundException as ex:
            raise FacilitiesNotFoundException from ex

