import gql

class BatchClient(gql.Client):
  def execute(self, document, *args, **kwargs):
    if self.schema:
      self.validate(document)

    return self._get_result(document, *args, **kwargs)