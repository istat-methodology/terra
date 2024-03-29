from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def orm_setup(db_settings: dict):
    engine = create_engine(f'{db_settings["DB_PROVIDER"]}://{db_settings["DB_USER"]}:{db_settings["DB_PASS"]}@{db_settings["DB_SERVER"]}/{db_settings["DB_NAME"]}?driver={db_settings["DB_DRIVER"]}')
    #Base.metadata.bind = engine
    #Base.metadata.create_all(engine)
    return engine

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