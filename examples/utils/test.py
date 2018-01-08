import fetch_method
import ctypes

f = fetch_method.FetchMethod()
import pdb
def get_arg_props(node):
  n = node['type']
  is_required = (n['kind'] == 'NON_NULL')
  while not n['name']:
    n = n['ofType']
    is_required = is_required or (n['kind'] == 'NON_NULL')
  return n['name'], is_required

def get_field_props(node):
  n = node['type']
  while not n['name']:
    n = n['ofType']
  return n

class StrWrap(object):
  def __init__(self, s):
    self.s = s

  def __add__(self, item):
    self.s += item
    return self


def get_fields(fm, fields, tab):
  depth = 0
  stack = []
  max_depth = 10000
  i = 0
  n = len(fields)
  txt = StrWrap('')
  stack.append((fields, tab, i, n))
  membersa = set()
  while len(stack) > 0 and depth < max_depth:
    depth += 1
    if i >= n:
      txt += '%s}' % tab
      (fields, tab, i, n) = stack.pop()
      #membersa.remove(fields[i]['name'])
      i += 1
      txt += '\n'
      continue
    field = fields[i]
    if 'description' in field and field['description']:
      txt += '%s# %s\n' % (tab+'  ', field['description'])
    txt += '%s%s' % (tab+'  ', field['name'])
    if field['type']['kind'] == 'LIST' or field['type']['kind'] == 'OBJECT':
      fprops = get_field_props(field)
      ftype = fm.get_type(fprops['name'], fprops['kind'])
      if 'fields' in ftype and ftype['fields']:
        if not field['name'] in membersa:
          membersa.add(field['name'])
          stack.append((fields, tab, i, n))
          fields = ftype['fields']
          tab += '  '
          i = 0
          n = len(ftype['fields'])
          txt += ' {\n'
          continue
      else:
        i += 1
        txt += '\n'
        continue
    i += 1
    txt += '\n'
    continue
  return txt.s

fout = open('queries.graphql', 'w')

for m in f.get_type('Query', 'OBJECT')["fields"]:
  txt = 'query '
  if 'args' in m and m['args']:
    txt += 'get%s(' % (m['name'][0].upper() + m['name'][1:])
    arg_list = []
    inner_arg_list = []
    for arg in m['args']:
      type_name, is_required = get_arg_props(arg)
      b = '!' if is_required else ''
      arg_param = '$%s: %s%s' % (arg['name'], type_name, b)
      if arg['defaultValue']:
        arg_param += ' = %s' % arg['defaultValue']
      arg_list.append(arg_param)
      inner_arg_list.append('%s: $%s' % (arg['name'],arg['name']))
    txt += ', '.join(arg_list)
    txt += ') {\n  '
  else:
    txt += 'get%s' % (m['name'][0].upper() + m['name'][1:])
    txt += ' {\n  '
  if 'description' in m and m['description']:
      txt += '# %s\n  ' % (m['description'])
  txt += '%s(%s) {\n' % (m['name'], ', '.join(inner_arg_list))

  try:
    fields = f.get_type(m['type']['name'], m['type']['kind'])['fields']
    if fields:
      txt += get_fields(f, fields, '  ')
  except Exception as e:
    txt += '  }\n'
    print(e)
  txt += '}'
  fout.write(txt+'\n\n')

for m in f.get_type('Mutation', 'OBJECT')["fields"]:
  txt = 'mutation '
  if 'args' in m and m['args']:
    txt += 'get%s(' % (m['name'][0].upper() + m['name'][1:])
    arg_list = []
    inner_arg_list = []
    for arg in m['args']:
      type_name, is_required = get_arg_props(arg)
      b = '!' if is_required else ''
      arg_param = '$%s: %s%s' % (arg['name'], type_name, b)
      if arg['defaultValue']:
        arg_param += ' = %s' % arg['defaultValue']
      arg_list.append(arg_param)
      inner_arg_list.append('%s: $%s' % (arg['name'],arg['name']))
    txt += ', '.join(arg_list)
    txt += ') {\n  '
  else:
    txt += 'get%s' % (m['name'][0].upper() + m['name'][1:])
    txt += ' {\n  '
  if 'description' in m and m['description']:
      txt += '# %s\n  ' % (m['description'])
  txt += '%s(%s) {\n' % (m['name'], ', '.join(inner_arg_list))
  try:
    fields = f.get_type(m['type']['name'], m['type']['kind'])['fields']
    if fields:
      txt += get_fields(f, fields, '  ')
    else:
      txt += '  }\n'
  except Exception as e:
    txt += '  }\n'
    print(e)
  txt += '}\n'
  fout.write(txt+'\n\n')

fout.close()
# exec(open('./test.py').read())