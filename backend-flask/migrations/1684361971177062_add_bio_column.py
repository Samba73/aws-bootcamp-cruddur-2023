class AddBioColumnMigration:
  def migrate_sql():
    data = """
    """
    return data
  def rollback_sql():
    data = """
    """
    return data
  def migrate():
    query_insert(AddBioColumnMigration.migrate_sql(),{
    })
  def rollback():
    query_insert(AddBioColumnMigration.rollback_sql(),{
    })
    
migration = AddBioColumnMigration    