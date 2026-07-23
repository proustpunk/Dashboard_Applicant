import {
    createContext,
    useContext,
    useState
} from "react";


const AuthContext = createContext<any>(null);


export function AuthProvider({
    children
}:{
    children: React.ReactNode
}){

    const [token,setToken] = useState(
        localStorage.getItem("token")
    );


    function login(token:string){

        localStorage.setItem(
            "token",
            token
        );

        setToken(token);
    }


    function logout(){

        localStorage.removeItem("token");
        setToken(null);
    }


    return (
        <AuthContext.Provider
            value={{
                token,
                login,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    )
}


export function useAuth(){
    return useContext(AuthContext);
}