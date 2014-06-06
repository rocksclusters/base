


from sqlalchemy import create_engine
import sqlalchemy
import mappings.base



#
# dump mysql code
#
def dump(sql, *multiparams, **params):
    print sql.compile(dialect=engine.dialect)


engine = create_engine('mysql://', strategy='mock', executor=dump)
mappings.base.Base.metadata.create_all(engine, checkfirst=False)

