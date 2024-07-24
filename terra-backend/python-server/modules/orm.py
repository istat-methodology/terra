from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def orm_setup(db_settings: dict):
    connection_string = db_settings['CONNECTION_STRING']
    engine = create_engine(connection_string)
    return engine

class countryEU(Base):
    __tablename__ = 'z_eu_country'

    CODE = Column(String, primary_key=True)
    DAT_INI = Column(Integer)
    DAT_FIN = Column(Integer)

class CPAIntra(Base):
    __tablename__ = 'cpa_intra'

    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    PRODUCT = Column(String, primary_key=True)
    PERIOD = Column(Integer, primary_key=True)
    VALUE_IN_EUROS = Column(Integer)

class CPATrim(Base):
    __tablename__ = 'cpa_trim'

    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    PRODUCT = Column("cpa", String, primary_key=True)
    PERIOD = Column("trimestre", String, primary_key=True)
    VALUE_IN_EUROS = Column("val_cpa", Integer)
    QUANTITY_IN_KG = Column("q_kg", Integer)

class trExtraUE(Base):
    __tablename__ = 'tr_extra_ue'

    PRODUCT = Column("product_nstr", String, primary_key=True)
    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    PERIOD = Column(Integer, primary_key=True)
    TRANSPORT_MODE = Column(Integer, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    VALUE_IN_EUROS = Column(Integer)
    QUANTITY_IN_KG = Column(Integer)

class trExtraUETrim(Base):
    __tablename__ = 'tr_extra_ue_trim'

    PRODUCT = Column("product_nstr", String, primary_key=True)
    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    PERIOD = Column("trimestre", String, primary_key=True)
    TRANSPORT_MODE = Column(String, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    VALUE_IN_EUROS = Column(Integer)
    QUANTITY_IN_KG = Column(Integer)

class comextImp(Base):
    __tablename__ = 'comext_imp'

    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    PRODUCT = Column("cpa", String, primary_key=True)
    PERIOD = Column(Integer, primary_key=True)
    VALUE_IN_EUROS = Column("val_cpa", Integer)
    QUANTITY_IN_KG = Column("q_kg", Integer)

class comextExp(Base):
    __tablename__ = 'comext_exp'

    DECLARANT_ISO = Column(String, primary_key=True)
    PARTNER_ISO = Column(String, primary_key=True)
    FLOW = Column(Integer, primary_key=True)
    PRODUCT = Column("cpa", String, primary_key=True)
    PERIOD = Column(Integer, primary_key=True)
    VALUE_IN_EUROS = Column("val_cpa", Integer)
    QUANTITY_IN_KG = Column("q_kg", Integer)