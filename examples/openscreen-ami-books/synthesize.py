from pathlib import Path
import importlib.util
p=Path(__file__).parent.parent/'remotion-contract-execution/synthesize.py'
spec=importlib.util.spec_from_file_location('pinned_voice',p);voice=importlib.util.module_from_spec(spec);spec.loader.exec_module(voice)
voice.LINES=[('opening','The work behind a commodity deal starts with understanding the market.',.5),('library','Explore practical guides to brokerage, spot markets, and the tools that connect them.',6.5),('brokerage','From grains and oilseeds to logistics, basis, and risk. Choose the guide for your work.',14),('execution','Follow the deal through documents, delivery, payment, and contract closeout.',22),('languages','Find English and Ukrainian editions, with downloadable formats shown for each book.',29.5),('cta','Explore the library at books dot one D three X dot com.',36)]
if __name__=='__main__':voice.main(base=Path(__file__).parent)
