import ujson


class FetchMethod(object):
  def __init__(self, filename='schema.json'):
    self.index = {}
    fp = open(filename)
    self.schema = ujson.load(fp)

    for type_data in self.schema['data']['__schema']['types']:
      kind = type_data['kind']
      name = type_data['name']

      if kind not in self.index:
        self.index[kind] = {}

      self.index[kind][name] = type_data

    fp.close()

  def get_type(self, name, kind=None):
    if kind:
      if kind not in self.index:
        raise Exception("Kind doesnt exist.")
      if name not in self.index[kind]:
        raise Exception("Specified Kind, Name doesnt exist.")
      return self.index[kind][name]
    else:
      result = []
      for kind in self.index:
        if name in self.index[kind]:
          result.append(self.index[kind][name])
      if len(result) == 0:
        raise Exception("Type not found.")
      elif len(result) == 1:
        return result[0]
      else:
        return result

  def get_kinds(self):
    return self.index.keys()

  def get_names(self):
    result = set()
    for kind in self.index:
      result.update(self.index[kind].keys())
    return list(result)