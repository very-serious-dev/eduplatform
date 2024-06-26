import { useState } from "react";
import { useNavigate } from "react-router-dom";
import EduAPIFetch from "../../client/EduAPIFetch";
import LoadingHUD from "../components/common/LoadingHUD";

const LoginPage = () => {
    const [isLoading, setLoading] = useState(false);
    const [error, setError] = useState(null)
    const [formUser, setFormUser] = useState("");
    const [formPassword, setFormPassword] = useState("");
    const navigate = useNavigate();
    
    const onSubmitLogin = (e) => {
        e.preventDefault();
        const options = {
            method: "POST",
            body: JSON.stringify({
                username: formUser,
                password: formPassword,
            }),
            credentials: "include"
        };
        setLoading(true);
        setError(null);
        EduAPIFetch("/api/v1/sessions", options)
                .then(json => {
                    setLoading(false);
                    if (json.success === true) {
                        navigate("/");
                    } else {
                        setError("Se ha producido un error");
                    }
                })
                .catch(error => {
                    setLoading(false);
                    setError(error.error ?? "Se ha producido un error");
                })
    }

    return <div className="loginMain">
        <img src="/logo.png" className="loginLogo"/>
        <div className="loginContainer card">
            <form onSubmit={onSubmitLogin}>
                <div className="formInput">
                    <input type="text" value={formUser} 
                      onChange={e => { setFormUser(e.target.value) }} 
                      required />
                    <div className="underline"></div>
                    <label htmlFor="">Usuario</label>
                </div>
                <div className="formInput">
                    <input type="password" value={formPassword}
                      onChange={e => { setFormPassword(e.target.value) }}
                      required />
                    <div className="underline"></div>
                    <label htmlFor="">Contraseña</label>
                </div>
                <div className="formSubmit">                    
                    <input type="submit" value="Login" />
                </div>
                { isLoading &&
                    <div className="loginHUDCentered"><LoadingHUD /></div>
                }
            </form>
        </div>
        { error !== null &&
            <div className="loginErrorContainer card">{error}</div>
        }
    </div>
}

export default LoginPage;