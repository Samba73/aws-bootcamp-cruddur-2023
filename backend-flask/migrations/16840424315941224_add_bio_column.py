from lib.db import query_insert
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
    query_insert(AddBioColumnMigration.migrate_sql(),{
    })
  def rollback():
    query_insert(AddBioColumnMigration.rollback_sql(),{
    })
    
migration = AddBioColumnMigration    