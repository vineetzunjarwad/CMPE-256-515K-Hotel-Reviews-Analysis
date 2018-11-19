import React from 'react';
import { Row, Col } from 'antd';
import basicStyle from './basicStyle';
import { rtl } from './withDirection';
import { Button } from 'antd';
import './table.css';

// import Select, { SelectOption } from '../../../components/uielements/select';
// import { Col, Row } from 'antd';
// const Option = SelectOption;
const { rowStyle, colStyle, gutter } = basicStyle;
      const marginStyle = {
        margin: rtl === 'rtl' ? '0 0 10px 10px' : '0 10px 10px 0'
      };

      // <style>
      // {
      //     font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
      //     border-collapse: collapse;
      //     width: 100%;
      // }
      //
      // td, th {
      //     border: 1px solid #ddd;
      //     padding: 8px;
      // }
      //
      // #customers tr:nth-child(even){background-color: #f2f2f2;}
      //
      // #customers tr:hover {background-color: #ddd;}
      //
      // #customers th {
      //     padding-top: 12px;
      //     padding-bottom: 12px;
      //     text-align: left;
      //     background-color: #4CAF50;
      //     color: white;
      // }
      // </style>

const user = (props)=>{

  let suggestionlist = [];
  if (props.suggestionlist !== undefined && props.suggestionlist.length!==0) {
    suggestionlist =<tbody className= "TableName">
    <tr className="Row">
    <th className ="Header">Hotel Name</th>
    <th className ="Header">Distance (in Miles)</th>
    <th className ="Header">Search</th>
    </tr>
    {props.suggestionlist.map ((userdata,index) => {
     let name = userdata[0];
     let distance = userdata[1];
    return (
    <tr className="Row">
    <td className="Element" >{name}</td>
    <td className="Element">{distance}</td>
    <td className="Element"><Button  style = {{fontSize:'20px'}} onClick={() => {props.hotelList(name)}}>Search Similar Hotels</Button></td>
    </tr>
  );
  })}</tbody>
 }

 return (
   <table >
   {suggestionlist}
   </table>
  );
}

export default user;
