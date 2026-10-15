from pathlib import Path
import importlib.util
p=Path(__file__).parent.parent/'remotion-contract-execution/synthesize.py'
s=importlib.util.spec_from_file_location('pinned_voice',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
v.LINES=[('opening','Every commodity deal connects a market, a product, and people.',.7),('market','Understand the physical market. How prices, basis, and logistics shape a real trade.',6.7),('brokerage','Build your brokerage skills, from the first offer to the terms that make a deal work.',13.7),('execution','Then take control of execution: documents, delivery, payments, and contract closeout.',20.7),('workspace','Explore the workspace behind the workflow, with the M N seven R Product Guide.',27.7),('languages','Find practical guides in English and Ukrainian, built for the work behind a commodity deal.',34.7),('library','Explore the books in one library. Choose the editions and formats that fit the way you learn.',42.7),('future','More books are coming. Explore the growing library at books dot one D three X dot com.',51.9)]
if __name__=='__main__':v.main(base=Path(__file__).parent)
