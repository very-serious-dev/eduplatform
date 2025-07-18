import { useState } from "react";
import { useNavigate } from "react-router";
import AdminBodyUsers from "./AdminBodyUsers";
import AdminBodyGroups from "./AdminBodyGroups";
import AdminBodyClasses from "./AdminBodyClasses";

const AdminBody = (props) => {
    const [currentTab, setCurrentTab] = useState("none");
    const navigate = useNavigate();

    const contentForCurrentTab = () => {
        if (currentTab === "users") {
            return <AdminBodyUsers groups={props.dashboardData.groups} onShouldRefresh={props.onShouldRefresh} />
        } else if (currentTab === "classes") {
            return <AdminBodyClasses groups={props.dashboardData.groups} onShouldRefresh={props.onShouldRefresh} />
        } else if (currentTab === "groups") {
            return <AdminBodyGroups groups={props.dashboardData.groups} onShouldRefresh={props.onShouldRefresh} />
        }
        return <div></div>
    }

    return <div className="adminMainBody">
            <div className="adminBodyColumn1">
                <div className="adminColumn1GoBack pointable card" onClick={() => { navigate("/"); }}>← Volver a inicio</div>
                <div className="adminColumn1MenuItem pointable card" onClick={() => { setCurrentTab("users"); }}>Usuarios ({props.dashboardData.usersCount})</div>
                <div className="adminColumn1MenuItem pointable card" onClick={() => { setCurrentTab("classes"); }}>Clases ({props.dashboardData.classesCount})</div>
                <div className="adminColumn1MenuItem pointable card" onClick={() => { setCurrentTab("groups"); }}>Grupos ({props.dashboardData.groups.length})</div>
            </div>
            <div className="adminBodyColumn2">
                <div className="adminBodyColumn2Content">
                    {contentForCurrentTab()}
                </div>
            </div>
        </div>
}

export default AdminBody;