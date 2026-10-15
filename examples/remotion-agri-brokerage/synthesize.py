from pathlib import Path
import importlib.util
b=Path(__file__).parent
p=b.parent/'remotion-contract-execution/synthesize.py'
spec=importlib.util.spec_from_file_location('pinned_supertonic',p);voice=importlib.util.module_from_spec(spec);spec.loader.exec_module(voice)
LINES=[('opening','A market needs more than a price.',.6),('conditions','Commodity, quality, delivery and price. The terms must fit.',6),('connect','A broker connects people, products and terms, from the first offer to the deal.',13.5),('title','Agri-Commodity Brokerage. A practical guide to grains and oilseeds markets.',22.6)]
validate_rows=voice.validate_rows
if __name__=='__main__':
 voice.LINES=LINES
 voice.main(base=b)
