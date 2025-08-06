#import nedded packages
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, DateTime, Float, Integer


Base=declarative_base()

"""
 Defines the 'Electricity' table schema for storing power
 generation, emissions, and market price data
"""
class Electric(Base):
    __tablename__='electricity_data'
    id=Column(Integer, primary_key=True, autoincrement=True)
    date=Column(DateTime)
    battery_charging_mv=Column(Float)
    pumps_mv=Column(Float)
    coal_brown_mv=Column(Float)
    coal_black_mv=Column(Float)
    bioenergy_biomass_mv=Column(Float)
    distillate_mv=Column(Float)
    gas_steam_mv=Column(Float)
    gas_ccgt_mv=Column(Float)
    gas_ocgt_mv=Column(Float)
    gas_reciprocating_mw=Column(Float)
    gas_waste_coal_mine_mw=Column(Float)
    battery_discharging_mw=Column(Float)
    hydro_mw=Column(Float)
    wind_mw=Column(Float) 
    solar_utility_mw=Column(Float)
    solar_rooftop_mw=Column(Float)
    coal_brown_emissions_vol_tco2e=Column(Float)
    coal_black_emissions_vol_tco2e=Column(Float)
    bioenergy_biomass_emissions_vol_tco2e=Column(Float)
    distillate_emissions_vol_tco2e=Column(Float)
    gas_steam_emissions_vol_tco2e=Column(Float)
    gas_ccgt_emissions_vol_tco2e=Column(Float)
    gas_ocgt_emissions_vol_tco2e=Column(Float)
    gas_reciprocating_emissions_vol_tco2e=Column(Float)
    gas_waste_coal_mine_emissions_vol_tco2e=Column(Float)
    emissions_intensity_kgco2e_per_mwh=Column(Float)
    price_aud_per_mwh=Column(Float)

    def __repr__(self):
        return {self.battery_charging_mv}