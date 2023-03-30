import { useState, useEffect, useRef } from "react";
import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import Form from 'react-bootstrap/Form';
import InputField from './InputField';
import { useApi } from '../contexts/ApiProvider';
import { useUser } from '../contexts/UserProvider';

export default function Write({ showStory }) {
    const [formErrors, setFormErrors] = useState({});
    const titleField = useRef();
    const api = useApi();
    const { user } = useUser();

    useEffect(() => {
        titleField.current.focus();
    }, []);

    // const onSubmit = async (e) => {
    //     e.preventDefault();
    //     const response = await api.post('/stories', {
    //         title: titleField.current.value
    //     });
    //     if (response.ok) {
    //         // showStory(response.body);
    //         // titleField
    //     }
    // }
}