import React, { Component } from 'react';
import './table.css';

const recommendation = (props)=>{

  let recommendationsList = []
  if (props.recommendList !== undefined && props.recommendList.length!==0) {
    recommendationsList = <div>
    <h1>Similar Hotel List</h1>
    {props.recommendList.map ((userdata,index) => {
    return (
    <li className ="List">{userdata}</li>
    );
  })}</div>
}

  return (
  <ol>
  {recommendationsList}
 </ol>
);


}


export default recommendation;
