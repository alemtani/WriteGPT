import { useState, useEffect, useRef } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useNavigate, useLocation } from "react-router-dom";
import Body from '../components/Body';
import InputField from "../components/InputField";
import { useApi } from "../contexts/ApiProvider";
import { useFlash } from "../contexts/FlashProvider";

export default function ResetPage() {
    const [formErrors, setFormErrors] = useState({});
    const passwordField = useRef();
    const password2Field = useRef();
    const navigate = useNavigate();
    const { search } = useLocation();
    const api = useApi();
    const flash = useFlash();
    const token = new URLSearchParams(search).get('token');

    useEffect(() => {
        if (!token) {
            navigate('/');
        } else {
            passwordField.current.focus();
        }
    }, [token, navigate]);

    const onSubmit = async (e) => {
        e.preventDefault();
        const password = passwordField.current.value;
        const password2 = password2Field.current.value;

        const errors = {};
        if (!password) {
            errors.password = 'New password must not be empty.';
        }
        if (!password2) {
            errors.password2 = 'New password again must not be empty.';
        }
        if (password !== password2) {
            errors.password2 = "Passwords don't match.";
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        const response = await api.put(`/tokens/reset`, {
            token,
            new_password: password
        });
        setFormErrors({});
        if (!response.ok) {
            flash(response.body.message, 'danger');
        } else {
            flash('You have successfully reset your password!', 'success');
            navigate('/login');
        }
    };

    return (
        <Body>
            <h1>Reset Your Password</h1>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="password" label="New Password" type="password"
                    error={formErrors.password} fieldRef={passwordField} />
                <InputField
                    name="password2" label="New Password Again" type="password"
                    error={formErrors.password2} fieldRef={password2Field} />
                <Button variant="primary" type="submit">Reset Password</Button>
            </Form>
        </Body>
    )
}