from lib.db_new import db
class AddBioColumnMigration:
  def migrate_sql():
    data = """
    ALTER TABLE public.users ADD COLUMN bio text;
    """
    return data
  def rollback_sql():
    data = """
    ALTER TABLE public.users DROP COLUMN bio;
    """
    return data
  def migrate():
    db.query_insert(AddBioColumnMigration.migrate_sql(),{
    })
  def rollback():
    db.query_insert(AddBioColumnMigration.rollback_sql(),{
    })
    
migration = AddBioColumnMigration    