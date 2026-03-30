import React, { useEffect, useState } from 'react';
import './footer.scss';
import {service} from '@/service'
const PageFooter = () => {

  const [version, setVersion] = useState('');

  useEffect(() => {
    let mounted = true;

    service.root().then(res => {
      if (mounted) {
        setVersion(res.data.version);
      }
    }).catch(() => {
      if (mounted) {
        setVersion('unknown');
      }
    });

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className='page-footer'>
      <div className='proj-name'>
        选课系统
      </div>
      <div>
        版本  | {version}
      </div>
    </div>
  );
}

export default PageFooter;
