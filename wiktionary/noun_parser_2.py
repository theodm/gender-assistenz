from wikitextprocessor import Wtp, WikiNode, NodeKind

ctx = Wtp(num_threads=1, cache_file="C:\\Users\\Theo\\Desktop\\Projekte\\ggender\\wiktionary\\tmpdir")

def page_handler(model, title, text):
   print(title)

   if model != "wikitext" or title.startswith("Template:"):
       return None

   tree = ctx.parse(text, pre_expand=True)

   return None


res = ctx.process("dewiktionary-20210601-pages-articles.xml", page_handler)

for r in res:
    print(r)