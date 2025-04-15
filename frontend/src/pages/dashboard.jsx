import React from "react";
import Welcome from "../components/welcome";
import Navbar from "../components/navbar";
import UploadSection from "../components/upload_section";

function DashBoard(){
    return (
    <>
    <div>
        <Navbar/>
        <Welcome/>
        <UploadSection/>
    </div>
    </>);
}
export default DashBoard