/* The owner playlist is maintained newest-first;preserve deliberate navigation after initial load. */
(function(root){
  function choose(list,selected,keepSelection){
    const ids=[],nativeIndexes=[];
    if(Array.isArray(list))list.forEach((id,i)=>{if(typeof id==='string'&&/^[a-zA-Z0-9_-]{11}$/.test(id)){ids.push(id);nativeIndexes.push(i);}});
    if(!ids.length)return null;
    const previous=keepSelection?ids.indexOf(selected):-1;
    return {ids,nativeIndexes,index:previous<0?0:previous};
  }
  if(typeof module==='object'&&module.exports)module.exports={choose};
  else root.FramewrightPlaylist={choose};
})(typeof window==='undefined'?globalThis:window);
